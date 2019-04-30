from ... import constants
from ... util import files
from ... old import audio_io
import json, numpy as np, os

# A Score maps the names of a precis to the length of that precis.
SCORE = {
    'min': 69384,
    'mean': 4768222,
    #  'max': 70974540,
}

DELETE_ON_FAILURE = not False


def zeros(length):
    return np.zeros(shape=(length, 2), dtype='double')


def mix_source_cyclically_into_output(source, out, begin):
    """
    The source is mixed one or more times cyclically over the output.

    begin is the time start of the source within the entire piece.
    """

    source_index = 0              # The sample index in the source
    out_index = begin % len(out)  # The sample index in the output

    # We advance these two indices through the source and output in parallel.
    while True:
        # How many more samples are there in the source and output?
        source_remains = len(source) - source_index
        out_remains = len(out) - out_index

        if out_remains >= source_remains:
            # There is more space remaining in the output than there is source.
            # Copy all the remaining source to out, and we're done.
            out[out_index:out_index + source_remains] += source[source_index:]
            return

        # Copy only part of the remaining source to out, and loop.
        out[out_index:] += source[source_index:source_index + out_remains]
        source_index += out_remains

        # Each segment after the first starts writing at 0 in the output buffer
        out_index = 0


def make_precis(shard, score):
    outputs = {k: zeros(v) for k, v in score.items()}
    for file, (begin, end, rbegin, rend) in shard:
        source = audio_io.read(constants.source(file))
        if end - begin != len(source):
            raise ValueError('Wrong length %s' % [end, begin, len(source)])

        for out in outputs.values():
            mix_source_cyclically_into_output(source, out, begin)

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
