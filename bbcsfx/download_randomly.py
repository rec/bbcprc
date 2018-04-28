import itertools, os, random, subprocess, sys, time, traceback
from . import constants


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
    url = '%s/%s' % (constants.URL_ROOT, filename)
    outfile = '%s/%s' % (constants.SOURCE_DIR, filename)
    print('Downloading', filename, '-', len(missing) - 1, 'to go')
    cmd = ('curl', '-o', outfile, url)

    try:
        subprocess.check_output(cmd)
        print('\n', filename, '*** Downloaded')
    except KeyboardInterrupt:
        try:
            os.remove(outfile)
        except:
            pass
        raise
    except:
        traceback.print_exc()
        try:
            os.remove(outfile)
        except:
            pass


def get_missing_sources():
    while True:
        existing = get_waves_in_directory(constants.SOURCE_DIR)
        clips = get_waves_in_directory(constants.CLIP_DIR)
        if download(clips - existing):
            return


if __name__ == '__main__':
    get_missing_sources()
    # get_files(*sys.argv[1:])
