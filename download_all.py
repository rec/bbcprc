import itertools, os, subprocess, time

FIRST_INDEX = 7030001
DOWNLOAD_TIMEOUT = 2
FAILURE_TIMEOUT = 2

OUTPUT_DIR = 'sounds'
EXISTING = set(os.listdir(OUTPUT_DIR))
NONEXISTENT_FILE = 'nonexistent_file.txt'

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'


def get_files():
    try:
        nonexistent = open(NONEXISTENT_FILE).read()
    except FileNotFoundError:
        nonexistent = ''
        open(NONEXISTENT_FILE, 'w').write('')
    nonexistent = set(s.strip() for s in nonexistent.splitlines())

    for i in itertools.count():
        filename = '0%d.wav' % (FIRST_INDEX + i)
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
        except:
            with open(NONEXISTENT_FILE, 'a') as fp:
                fp.write(filename)
                fp.write('\n')
            time.sleep(FAILURE_TIMEOUT)


if __name__ == '__main__':
    get_files()
