from collections import Counter
from pathlib import Path
import statistics, yaml

CENSUS_FILE = 'results/census.yml'


def report():
    files = {}

    # How many files are there - 1 and 2?
    file_counter = Counter()
    file_frames = Counter()

    for r in yaml.safe_load_all(open(CENSUS_FILE)):
        filename = Path(r['filename']).stem
        frames, channels = r['nframes'], r['nchannels']
        files[filename] = frames
        file_counter[channels] += 1
        file_frames[channels] += frames

    # Longest and shortest files?
    shortest = min(files.items(), key=lambda x: x[1])
    longest = max(files.items(), key=lambda x: x[1])
    mean = statistics.mean(files.values())
    median = statistics.median(files.values())
    mode = statistics.mode(files.values())
    variance = statistics.pvariance(files.values())
    print(f"""
file_counter = {file_counter}
file_frames = {file_frames}
shortest = {shortest}
longest = {longest}
mean = {mean}
median = {median}
mode = {mode}
variance = {variance}
    """)

if __name__ == '__main__':
    report()
