import datetime, json, os, time, wave
import numpy as np
from . import constants, files


def to_duration(frames):
    seconds = frames / constants.FRAME_RATE
    duration = datetime.timedelta(seconds=seconds)
    return str(duration)


def report_durations():
    metadata_files = list(files.with_suffix(constants.METADATA_DIR, '.json'))

    d = {}
    for f in metadata_files:
        metadata = json.load(open(f))
        if not metadata:
            print('Empty file', f)
        for k, v in metadata.items():
            d.setdefault(k, []).append(v)

    frame_counts, rms, errors = d['frame_count'], d['rms'], d['error']

    print('Total number of files', len(metadata_files))
    print('Error count', len(errors))
    print('Successful files', len(frame_counts))

    total_length = sum(frame_counts)
    average_frame_count = total_length / len(frame_counts)
    print('Total length', to_duration(total_length))
    print('Average length', to_duration(average_frame_count))
    print('Min length', to_duration(min(frame_counts)))
    print('Max length', to_duration(max(frame_counts)))

    average_rms = sum(rms) / len(rms)
    print('Average rms', average_rms)
    print('Min rms', min(rms))
    print('Max rms', max(rms))
    errors = sorted(set(tuple(i) for i in errors))
    print('Errors', errors)


if __name__ == '__main__':
    report_durations()
