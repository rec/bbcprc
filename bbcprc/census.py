import sys, wave, yaml

from . import files

PARAMS = 'nchannels', 'sampwidth', 'framerate', 'nframes'
EXPECTED = {'comptype': 'NONE', 'compname': 'not compressed'}


def census(directory):
    def report(filename):
        with wave.open(filename) as fp:
            p = fp.getparams()
            for k, v in EXPECTED.items():
                new_v = getattr(p, k)
                if new_v != v:
                    files.error('Unexpected param value', k, new_v, filename)
            return {i: getattr(p, i) for i in PARAMS}

    def reports():
        for filename in files.wave_files(directory):
            try:
                yield report(filename)
            except:
                files.error('Exception on file', filename)
                traceback.print_exc(file=sys.stderr)

    yaml.safe_dump_all(reports(), sys.stdout)


if __name__ == '__main__':
    census(sys.argv[1])
