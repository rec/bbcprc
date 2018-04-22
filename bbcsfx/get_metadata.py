import datetime, json, os, time, wave
import numpy as np
from . import constants, to_npy


def get_metadata():
    output_files = os.listdir(constants.OUTPUT_DIR)
    output_files = [i for i in output_files if i.endswith('.wav')]

    metadata_files = os.listdir(constants.METADATA_DIR)
    metadata_files = [i[:-5] for i in metadata_files if i.endswith('.json')]

    missing = set(output_files) - set(metadata_files)
    print(len(missing), len(output_files), len(metadata_files))
    if True:
        return

    for filename in sorted(missing):
        if True:
            print('missing', filename)
            continue
        wave_file = os.path.join(constants.OUTPUT_DIR, filename)
        try:
            samples = to_npy.read(wave_file)
        except Exception as e:
            metadata = {'error': [str(e)] + list(e.args)}
        else:
            rms = np.sqrt(np.mean(np.square(samples)))
            metadata = {'frame_count': len(samples), 'rms': rms}

        metadata_file = os.path.join(constants.METADATA_DIR, filename + '.json')
        json.dump(metadata, open(metadata_file, 'w'))


if __name__ == '__main__':
    get_metadata()
