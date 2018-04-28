import collections, datetime, json, os, time, wave
import numpy as np
from . import constants, files


def to_duration(frames):
    seconds = frames / constants.FRAME_RATE
    duration = datetime.timedelta(seconds=seconds)
    return str(duration)


def report_durations():
    metadata_files = list(files.with_suffix(constants.METADATA_DIR, '.json'))

    frame_counts, rms, errors = [], [], {}
    for f in metadata_files:
        metadata = json.load(open(f))
        if not metadata:
            print('Empty file', f)
        elif 'error' in metadata:
            errors.setdefault(str(metadata['error']), []).append(f)
        else:
            frame_counts.append(metadata['frame_count'])
            rms.append(metadata['rms'])

    print('Total number of files', len(metadata_files))
    print('Error count', len(errors))
    print('Successful files', len(frame_counts))

    total_length = sum(frame_counts)
    average_frame_count = total_length / len(frame_counts)
    print('Total length', to_duration(total_length), total_length)
    print('Average length', to_duration(average_frame_count))
    print('Min length', to_duration(min(frame_counts)))
    print('Max length', to_duration(max(frame_counts)))

    average_rms = sum(rms) / len(rms)
    print('Average rms', average_rms)
    print('Min rms', min(rms))
    print('Max rms', max(rms))

    print(errors)
    for error, source_files in sorted(errors.items()):
        print(error)
        for f in source_files:
            print('  ', f)


if __name__ == '__main__':
    report_durations()
