from . import constants
import datetime
import json
import os


def to_duration(frames):
    seconds = frames / constants.FRAME_RATE
    duration = datetime.timedelta(seconds=seconds)
    return str(duration), frames


def report_durations():
    metadata_files = constants.metadata_files()

    frame_counts, rms, errors, everything = [], [], {}, {}
    files_to_frame_count = {}

    for f in metadata_files:
        metadata = json.load(open(f))
        everything[os.path.basename(f)] = metadata

        if not metadata:
            print('Empty file', f)
        elif 'error' in metadata:
            errors.setdefault(str(metadata['error']), []).append(f)
        else:
            frame_count = metadata['frame_count']
            files_to_frame_count[f] = frame_count
            frame_counts.append(frame_count)
            rms.append(metadata['rms'])

    print('Total number of files', len(metadata_files))
    print('Error count', len(errors))
    print('Successful files', len(frame_counts))

    total_length = sum(frame_counts)
    average_frame_count = total_length / len(frame_counts)
    print('Total length', *to_duration(total_length))
    print('Average length', *to_duration(average_frame_count))
    print('Min length', *to_duration(min(frame_counts)))
    print('Max length', *to_duration(max(frame_counts)))

    average_rms = sum(rms) / len(rms)
    print('Average rms', average_rms)
    print('Min rms', min(rms))
    print('Max rms', max(rms))

    for error, source_files in sorted(errors.items()):
        print(error)
        for f in source_files:
            print('  ', f)

    by_frame = sorted((v, k) for k, v in files_to_frame_count.items())

    N = 50

    if False:
        for frames in by_frame[:N], by_frame[-N:]:
            for count, file in frames:
                print(os.path.basename(file)[:-5], *to_duration(count))

            print()
            print('...')
            print()
        return

    for i, (count, file) in enumerate(by_frame):
        print('%05d' % i, os.path.basename(file)[:-5], *to_duration(count))


if __name__ == '__main__':
    report_durations()
