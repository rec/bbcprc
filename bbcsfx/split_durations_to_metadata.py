import json, os
from . import constants


def split_durations():
    data = json.load(open(constants.DURATION_FILE))
    for filename, (frame_count, rms) in data.items():
        meta = {'frame_count': frame_count, 'rms': rms}
        meta_filename = os.path.join(constants.METADATA_DIR, filename)
        json.dump(meta, open(meta_filename, 'w'))


if __name__ == '__main__':
    split_durations()
