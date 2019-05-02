from . import constants
import os
import random
import subprocess
import time
import traceback

MINIMUM_SIZE = 100000


def get_waves_in_directory(root):
    return {f for f in os.listdir(root) if f.endswith('.wav')}


def get_files():
    while True:
        existing = get_waves_in_directory(constants.SOURCE_DIR)
        all_filenames = {i.strip() for i in open(constants.ALL_FILENAMES)}
        download(all_filenames - existing)
        time.sleep(constants.TIMEOUT)


def download(missing):
    if not missing:
        return True

    filename = random.choice(list(missing))
    print('Downloading', filename, '-', len(missing) - 1, 'to go')
    download_one(filename)


def download_one(filename):
    url = '%s/%s' % (constants.URL_ROOT, filename)
    outfile = '%s/%s' % (constants.SOURCE_DIR, filename)
    cmd = ('curl', '-o', outfile, url)

    def remove():
        try:
            os.remove(outfile)
        except Exception:
            pass

    try:
        subprocess.check_output(cmd)
        if os.stat(outfile).st_size < MINIMUM_SIZE:
            print('ERROR:', filename, 'removed as too small')

            remove()
        else:
            print(filename, 'downloaded')

    except KeyboardInterrupt:
        remove()
        raise

    except Exception:
        traceback.print_exc()
        remove()


def get_missing_sources():
    while True:
        existing = get_waves_in_directory(constants.SOURCE_DIR)
        clips = get_waves_in_directory(constants.CLIP_DIR)
        if download(clips - existing):
            return


if __name__ == '__main__':
    get_missing_sources()
    # get_files(*sys.argv[1:])
