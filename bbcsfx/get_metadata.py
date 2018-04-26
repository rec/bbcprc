import json, os, time, wave
import numpy as np
from . import constants, audio_io, worker

PROCESS_COUNT = 2


def write_metadata_for_one_file(filename):
    wave_file = os.path.join(constants.OUTPUT_DIR, filename)
    try:
        samples = audio_io.read(wave_file)
    except Exception as e:
        metadata = {'error': [str(e)] + list(e.args)}
    else:
        metadata = {
            'frame_count': len(samples),
            'rms': np.sqrt(np.mean(np.square(samples))),
        }

    metadata_file = os.path.join(constants.METADATA_DIR, filename + '.json')
    json.dump(metadata, open(metadata_file, 'w'), sort_keys=True)


def get_missing():
    output_files = os.listdir(constants.OUTPUT_DIR)
    output_files = [i for i in output_files if i.endswith('.wav')]

    metadata_files = os.listdir(constants.METADATA_DIR)
    metadata_files = [i[:-5] for i in metadata_files if i.endswith('.json')]

    missing = sorted(set(output_files) - set(metadata_files))
    print('Missing:', len(missing), 'Metadata:', len(metadata_files),
          'Total:', len(output_files))

    return missing


def get_metadata():
    with worker.Workers(PROCESS_COUNT) as workers:
        for filename in sorted(get_missing()):
            workers.run(write_metadata_for_one_file, filename)


def fix_files():
    os.chdir(constants.METADATA_DIR)
    for f in os.listdir('.'):
        data = json.load(open(f))
        json.dump(data, open(f, 'w'), sort_keys=True)


if __name__ == '__main__':
    fix_files()
    # get_metadata()
