from .. import constants
from collections import Counter
from pathlib import Path
import statistics
import sys
import yaml

CENSUS_FILE = 'results/census.yml'


def report():
    files = {}

    # How many files are there - 1 and 2?
    file_counter = Counter()
    file_seconds = Counter()
    frame_counter = Counter()

    for r in yaml.safe_load_all(open(CENSUS_FILE)):
        filename = Path(r['filename']).stem
        frames = r['nframes']
        frame_counter[frames] += 1
        seconds = frames / constants.FRAMERATE
        channels = r['nchannels']
        files[filename] = seconds
        file_counter[channels] += 1
        file_seconds[channels] += seconds

    count_counter = {}
    for frames, count in frame_counter.items():
        count_counter.setdefault(count, []).append(frames)

    return {
        'shortest': list(min(files.items(), key=lambda x: x[1])),
        'longest': list(max(files.items(), key=lambda x: x[1])),
        'mean': statistics.mean(files.values()),
        'median': statistics.median(files.values()),
        'mode': statistics.mode(files.values()),
        'stdev': statistics.pstdev(files.values()),
        'file_counter': dict(file_counter),
        'count_counter': count_counter,
        'frame_counter': dict(frame_counter),
    }


if __name__ == '__main__':
    yaml.dump(report(), sys.stdout)
