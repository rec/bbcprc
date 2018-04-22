import datetime, json, os, time, wave
import numpy as np
from . import constants, to_npy


def get_sizes():
    existing = set(os.listdir(constants.OUTPUT_DIR))
    try:
        sizes = json.load(open(constants.DURATION_FILE))
        # sizes = {}
    except:
        sizes = {}

    for filename in sorted(existing - set(sizes)):
        try:
            fn = os.path.join(constants.OUTPUT_DIR, filename)
            samples = to_npy.read(fn)
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

        seconds = len(samples) / constants.FRAME_RATE
        duration = datetime.timedelta(seconds=seconds)
        print(filename, str(duration), len(samples), rms / 0x8000)

        with open(constants.DURATION_FILE, 'w') as fp:
            json.dump(sizes, fp, indent=4, sort_keys=True)
        # break


if __name__ == '__main__':
    get_sizes()
