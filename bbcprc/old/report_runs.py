from . import constants, download
import os


def to_runs(files):
    # https://stackoverflow.com/a/37793316/43839
    k = 0
    new_list = [[]]
    for i, file in enumerate(files):
        if file not in new_list[max(k - 1, 0)]:
            new_list[k].append(file)
            for j in range(i + 1, len(files)):
                if files[j] - file == j - i and files[j] not in new_list[k]:
                    new_list[k].append(files[j])
            k += 1
            new_list.append([])

    if new_list and not new_list[-1]:
        new_list.pop()

    return new_list


def report_runs():
    previous = ''
    for run in get_source_runs():
        gap = previous and ('(%s)' % (run[0] - previous - 1))
        previous = run[-1]
        if len(run) == 1:
            print(previous, gap)
        else:
            print(run[0], '-', previous, gap)


def to_index(filename):
    # Filenames look like 00008000.wav
    return int(filename.split('.')[0].lstrip('0'))


def to_filename(index):
    return '%08d.wav' % index


def get_source_runs():
    files = os.listdir(constants.SOURCE_DIR)
    files = [to_index(f) for f in files if f.endswith('.wav')]
    files.sort()
    return to_runs(files)


def get_edge_files():
    indexes = set()
    for run in get_source_runs():
        indexes.add(run[0] - 1)
        indexes.add(run[-1] + 1)

    return [to_filename(i) for i in sorted(indexes)]


if __name__ == '__main__':
    for f in get_edge_files():
        download.download_one(f)
