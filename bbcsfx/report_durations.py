import datetime, json, os, time, wave
import numpy as np
from . import constants, files, to_npy


def to_duration(frames):
    seconds = frames / constants.FRAME_RATE
    duration = datetime.timedelta(seconds=seconds)
    return str(duration)


def report_durations():
    metadata_files = list(files.with_suffix(constants.METADATA_DIR, '.json'))

    d = {}
    for f in metadata_files:
        for k, v in json.load(open(f)).items():
            d.setdefault(k, []).append(v)

    print('Number of files', len(metadata_files))
    average_frame_count = sum(d['frame_count']) / len(d['frame_count'])
    print('Average length', to_duration(average_frame_count))
    print('Min length', to_duration(min(d['frame_count'])))
    print('Max length', to_duration(max(d['frame_count'])))

    average_rms = sum(d['rms']) / len(d['rms'])
    print('Average rms', average_rms)
    print('Min rms', min(d['rms']))
    print('Max rms', max(d['rms']))
    print('Error count', len(d['error']))
    errors = sorted(set(tuple(i) for i in d['error']))
    print('Errors', errors)


if __name__ == '__main__':
    report_durations()
