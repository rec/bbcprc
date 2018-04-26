import time, traceback
import multiprocessing as mp


class Worker(mp.Process):
    def __init__(self, queue, counter, use_logging=False):
        super().__init__()
        self.time = time.time()
        self.queue = queue
        self.counter = counter
        self.use_logging = use_logging

    def run(self):
        for command, *args in iter(self.queue.get, None):
            try:
                command(*args)
            except Exception as e:
                name = getattr(command, '__name__', str(command))
                print('ERROR on command', name, args, e)
                traceback.print_exc()
            else:
                counter = self._increment_counter()
                if self.use_logging:
                    self._log(command, args, counter)

    def _increment_counter(self):
        with self.counter.get_lock():
            self.counter.value += 1
            return self.counter.value

    def _log(self, command, args, counter):
        delta_t = time.time() - self.time
        average = delta_t / counter

        command = getattr(command, '__name__', str(command))
        msg = '{command}{args} -> {counter} ({average})'
        print(msg.format(**locals()))


class Workers:
    def __init__(self, count=4):
        self.queue = mp.Queue()
        self.counter = mp.Value('i')
        self.workers = [Worker(self.queue, self.counter) for i in range(count)]

    def __enter__(self):
        for w in self.workers:
            w.start()
        return self

    def __exit__(self, type, value, traceback):
        for w in self.workers:
            self.queue.put(None)

    def run(self, *args):
        self.queue.put(args)
