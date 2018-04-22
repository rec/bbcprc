import datetime, json, os, time, wave
import numpy as np
from . import to_npy

DURATION_FILE = 'durations.json'
OUTPUT_DIR = '/Volumes/Bach/disks/bbcsfx'
EXISTING = set(os.listdir(OUTPUT_DIR))
WRITE_CUTOFF = 20
ATTRIBUTES = 'sample_width', 'frame_rate', 'duration_seconds'


def get_sizes():
    try:
        sizes = json.load(open(DURATION_FILE))
        # sizes = {}
    except:
        sizes = {}

    for filename in sorted(EXISTING - set(sizes)):
        try:
            samples = to_npy.read(os.path.join(OUTPUT_DIR, filename))
        except wave.Error:
            # print('Not a wave file:', filename)
            continue
        except AssertionError:
            # print('Not stereo', filename)
            continue
        except:
            # Possibly odd number of samples, report this
            continue


        rms = np.sqrt(np.mean(np.square(samples)))
        sizes[filename] = len(samples), rms

        seconds = len(samples) / 44100
        duration = datetime.timedelta(seconds=seconds)
        print(filename, str(duration), len(samples), rms / 0x8000)

        with open(DURATION_FILE, 'w') as fp:
            json.dump(sizes, fp, indent=4, sort_keys=True)
        # break


if __name__ == '__main__':
    get_sizes()
