from .. import audio_io, constants, files
import json, numpy as np, os, random, shutil

SCORE = {
    'min': 69384,
    'mean': 4768222,
    #  'max': 70974540,
}

DELETE_ON_FAILURE = not False


def make_precis(shard, score):
    def zeros(length):
        return np.zeros(shape=(length, 2), dtype='double')

    outputs = {k: zeros(v) for k, v in score.items()}
    for file, (begin, end, rbegin, rend) in shard:
        source = audio_io.read(constants.source(file))
        if end - begin != len(source):
            raise ValueError('Wrong length %s' % [end, begin, len(source)])

        for out in outputs.values():
            # The source is printed one or more times cyclically over the
            # output, starting at location "begin".
            i_source = 0
            i_out = begin % len(out)

            while True:
                source_remains = len(source) - i_source
                out_remains = len(out) - i_out

                if out_remains >= source_remains:
                    # Copy all the remaining source to out, and we're done.
                    segment = source[i_source:] if i_source else source
                    out[i_out:i_out + source_remains] += segment
                    break

                # Copy only part of the remaining source to out.
                out[i_out:] += source[i_source:i_source + out_remains]
                i_source += out_remains

                # Each segment after the first starts at 0 in the output.
                i_out = 0

    return outputs


def precis(score=SCORE):
    schedule = json.load(open('results/schedule.json'))
    for i, shard in enumerate(schedule):
        shard_file = constants.shard('precis', i)
        if not os.path.exists(shard_file):
            break
    else:
        # All done!
        return

    with files.delete_on_fail(shard_file, 'wb') as fp:
        precis = make_precis(shard, score)
        np.save(fp, precis)
        print('Written', shard_file)

    return shard_file


def to_wave_files(shard_file):
    precis = np.load(shard_file).item()
    for name, out in precis.items():
        wave_file = shard_file + '.' + name + '.wav'
        audio_io.write(wave_file, out)


if __name__ == '__main__':
    shard_file = precis()
    to_wave_files(shard_file)
