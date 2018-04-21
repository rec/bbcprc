import itertools, os, subprocess, sys, time, traceback

TIMEOUT = 2

OUTPUT_DIR = '/Volumes/Bach/disks/bbcsfx'
EXISTING = set(os.listdir(OUTPUT_DIR))

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'


def get_files(index=0, parts=1):
    index, parts = int(index), int(parts)
    files = [i.strip() for i in open('all_filenames.txt')]
    r = len(files) / parts
    begin, end = int(index * r), int((index + 1) * r)
    print('begin', begin, files[begin])
    print('end', end - 1, files[end - 1])

    for i in range(begin, end):
        filename = files[i].strip()
        if filename in EXISTING:
            continue

        url = '%s/%s' % (URL_ROOT, filename)
        outfile = '%s/%s' % (OUTPUT_DIR, filename)
        print(filename, end=' ', flush=True)
        cmd = ('curl', '-o', outfile, url)

        try:
            subprocess.check_output(cmd)
            print('\n', filename, '*** Downloaded')
        except KeyboardInterrupt:
            try:
                os.remove(outfile)
                print('*** Removed', outfile)
            except:
                print('*** FAILED to remove', outfile)
            raise
        except:
            traceback.print_exc()
        time.sleep(TIMEOUT)


if __name__ == '__main__':
    get_files(*sys.argv[1:])
