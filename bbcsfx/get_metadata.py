import json, os, time, wave
import numpy as np
import multiprocessing as mp
from . import constants, to_npy

PROCESS_COUNT = 2


def write_metadata_for_one_file(filename):
    wave_file = os.path.join(constants.OUTPUT_DIR, filename)
    try:
        samples = to_npy.read(wave_file)
    except Exception as e:
        metadata = {'error': [str(e)] + list(e.args)}
    else:
        metadata = {
            'frame_count': len(samples),
            'rms': np.sqrt(np.mean(np.square(samples))),
        }

    metadata_file = os.path.join(constants.METADATA_DIR, filename + '.json')
    json.dump(metadata, open(metadata_file, 'w'))


class Worker(mp.Process):
    def __init__(self, queue, counter,
                 perform_work=write_metadata_for_one_file):
        super().__init__()
        self.time = time.time()
        self.queue = queue
        self.counter = counter
        self.perform_work = perform_work

    def run(self):
        for filename in iter(self.queue.get, None):
            self.perform_work(filename)
            delta_t = time.time() - self.time
            with self.counter.get_lock():
                self.counter.value += 1
                counter = self.counter.value
            average = delta_t / counter
            print('{filename} -> {counter} ({average})'.format(**locals()))


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
    missing = get_missing()

    if not missing:
        return

    # https://stackoverflow.com/a/9039979/43839
    queue = mp.Queue()
    for i in missing:
        queue.put(i)

    counter = mp.Value('i')
    t = time.time()
    workers = [Worker(queue, counter) for i in range(PROCESS_COUNT)]

    print('starting...')
    for w in workers:
        queue.put(None)
        w.start()


if __name__ == '__main__':
    # get_missing()
    get_metadata()
