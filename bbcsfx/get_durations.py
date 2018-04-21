import datetime, json, os, pydub, time

DURATION_FILE = 'durations.json'
OUTPUT_DIR = '/Volumes/Bach/disks/bbcsfx'
EXISTING = set(os.listdir(OUTPUT_DIR))
WRITE_CUTOFF = 20
ATTRIBUTES = 'sample_width', 'frame_rate', 'duration_seconds'


def get_sizes_once():
    try:
        sizes = json.load(open(DURATION_FILE))
    except:
        sizes = {}

    for filename in sorted(EXISTING - set(sizes)):

        basename = os.path.basename(filename)

            seg = pydub.AudioSegment.from_file(filepath)
            frame_count = int(seg.frame_count())
            sizes[filename] = frame_count
            duration = datetime.timedelta(seconds=seg.duration_seconds)
            print(filename, str(duration), frame_count)

    with open(DURATION_FILE, 'w') as fp:
        json.dump(sizes, fp, indent=4, sort_keys=True)


def get_sizes():
    while True:
        get_sizes_once()
        time.sleep(WRITE_CUTOFF)


if __name__ == '__main__':
    get_sizes()
