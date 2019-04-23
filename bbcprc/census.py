import sys, wave, yaml

PARAMS = 'nchannels', 'sampwidth', 'framerate', 'nframes'
EXPECTED = {'comptype': 'NONE', 'compname': 'not compressed'}


def census(directory):
    def error(*args):
        print('ERROR:', *args, file=sys.stderr)

    def report(filename):
        with wave.open(filename) as fp:
            p = fp.getparams()
            for k, v in EXPECTED.items():
                new_v = getattr(p, k)
                if new_v != v:
                    error('Unexpected param value', k, new_v, filename)
            return {i: getattr(p, i) for i in PARAMS}

    def reports():
        files = (f for f in Path(directory).iterdir() if w.suffix == 'wav')
        for filename in sorted(files):
            try:
                yield report(filename)
            except:
                print('Exception on file', filename, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    yaml.safe_dump_all(reports(), sys.stdout)


if __name__ == '__main__':
    census(sys.argv[1])
