import os
from . import constants


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
    def to_number(filename):
        return int(filename.split('.')[0].lstrip('0'))

    files = (f for f in os.listdir(constants.SOURCE_DIR) if f.endswith('.wav'))
    previous = ''
    for run in to_runs(sorted(to_number(f) for f in files)):
        gap = previous and ('(%s)' % (run[0] - previous - 1))
        previous = run[-1]
        if len(run) == 1:
            print(previous, gap)
        else:
            print(run[0], '-', previous, gap)


if __name__ == '__main__':
    report_runs()
