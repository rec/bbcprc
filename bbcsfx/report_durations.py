import datetime, json, os, time, wave
import numpy as np
from . import constants, to_npy


def to_duration(frames):
    seconds = frames / constants.FRAME_RATE
    duration = datetime.timedelta(seconds=seconds)
    return str(duration)


def report_durations():
    try:
        sizes = json.load(open(constants.DURATION_FILE))
    except:
        sizes = {}

    print('Number of files', len(sizes))
    frame_counts, rms = zip(*sizes.values())

    average_frame_count = sum(frame_counts) / len(frame_counts)
    print('Average length', to_duration(average_frame_count))
    print('Min length', to_duration(min(frame_counts)))
    print('Max length', to_duration(max(frame_counts)))

    average_rms = sum(rms) / len(rms)
    print('Average rms', average_rms)
    print('Min rms', min(rms))
    print('Max rms', max(rms))
    print(*sorted(rms)[:25], sep='\n')
    print('...')
    print(*sorted(rms)[-25:], sep='\n')


if __name__ == '__main__':
    report_durations()
