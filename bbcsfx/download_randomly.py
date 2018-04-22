import itertools, os, random, subprocess, sys, time, traceback

TIMEOUT = 2

OUTPUT_DIR = '/Volumes/Bach/disks/bbcsfx'
FILES = {i.strip() for i in open('all_filenames.txt')}
URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'


def get_files():
    while True:
        existing = {i for i in os.listdir(OUTPUT_DIR) if i.endswith('.wav')}

        missing = list(FILES - existing)
        if not missing:
            break

        filename = random.choice(missing)
        url = '%s/%s' % (URL_ROOT, filename)
        outfile = '%s/%s' % (OUTPUT_DIR, filename)
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
        time.sleep(TIMEOUT)


if __name__ == '__main__':
    get_files(*sys.argv[1:])
