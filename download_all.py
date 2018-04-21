import itertools, os, subprocess, sys, time

FIRST_INDEX = 7030001
DOWNLOAD_TIMEOUT = 6
FAILURE_TIMEOUT = 6

OUTPUT_DIR = '/Volumes/Bach/disks/bbcsfx'
EXISTING = set(os.listdir(OUTPUT_DIR))
NONEXISTENT_FILE = 'nonexistent_file.txt'

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'


def get_files(index=FIRST_INDEX):
    index = int(index)
    try:
        nonexistent = open(NONEXISTENT_FILE).read()
    except FileNotFoundError:
        nonexistent = ''
        open(NONEXISTENT_FILE, 'w').write('')
    nonexistent = set(s.strip() for s in nonexistent.splitlines())

    for i in itertools.count():
        filename = '0%d.wav' % (index + i)
        if filename in EXISTING or filename in nonexistent:
            continue

        url = '%s/%s' % (URL_ROOT, filename)
        outfile = '%s/%s' % (OUTPUT_DIR, filename)
        print(filename, end=' ', flush=True)
        cmd = ('curl', '-o', outfile, url)

        try:
            subprocess.check_output(cmd)
            print('\n', filename, '*** Downloaded')
            time.sleep(DOWNLOAD_TIMEOUT)
        except KeyboardInterrupt:
            try:
                os.remove(outfile)
                print('*** Removed', outfile)
            except:
                print('*** FAILED to remove', outfile)
            raise
        except:
            with open(NONEXISTENT_FILE, 'a') as fp:
                fp.write(filename)
                fp.write('\n')
            time.sleep(FAILURE_TIMEOUT)


if __name__ == '__main__':
    get_files(*sys.argv[1:])
