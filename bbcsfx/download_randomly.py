import itertools, os, random, subprocess, sys, time, traceback
from . import constants


def get_files():
    while True:
        existing = os.listdir(constants.OUTPUT_DIR)
        existing = {i for i in existing if i.endswith('.wav')}
        all_filenames = {i.strip() for i in open(constants.ALL_FILENAMES)}
        missing = list(all_filenames - existing)
        if not missing:
            break

        filename = random.choice(missing)
        url = '%s/%s' % (constants.URL_ROOT, filename)
        outfile = '%s/%s' % (constants.OUTPUT_DIR, filename)
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
        time.sleep(constants.TIMEOUT)


if __name__ == '__main__':
    get_files(*sys.argv[1:])
