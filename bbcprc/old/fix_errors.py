from . import constants, get_clips_and_metadata, worker
import json

SUFFIX = '.json'


def fix_errors(filename):
    if not filename.endswith(SUFFIX):
        return
    filename = filename[: -len(SUFFIX)]

    metadata_file = constants.metadata(filename)
    metadata = json.load(open(metadata_file))
    if 'error' not in metadata:
        return
    print('Fixing', filename)
    get_clips_and_metadata.fix_metadata(filename)


if __name__ == '__main__':
    worker.work_on_files(fix_errors, constants.METADATA_DIR)
