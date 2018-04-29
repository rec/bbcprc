import itertools, json, os, random, sys
from .. import constants


def get_score(piece_size=51):
    file_lengths = []
    for f in constants.metadata_files():
        metadata = json.load(open(f))
        if 'error' not in metadata:
            file = os.path.basename(f)[:-5]
            frame_count = metadata['frame_count']
            file_lengths.append((frame_count, file))

    score = {}

    def add():
        lengths, files = zip(*file_lengths)
        ends = list(itertools.accumulate(lengths))
        begins = ([0] + ends)[:-1]

        for f, b, e in zip(files, begins, ends):
            score.setdefault(f, []).extend([b, e])
    file_lengths.sort()
    add()
    file_lengths.reverse()
    add()
    assert(all(len(i) == 4 for i in score.values()))

    score = list(score.items())
    random.shuffle(score)

    assert not (len(score) % piece_size)
    pieces = len(score) // piece_size
    for i in range(pieces):
        yield score[piece_size * i:piece_size * (i + 1)]


if __name__ == '__main__':
    fp = open(sys.argv[1], 'w') if len(sys.argv) > 1 else sys.stdout
    json.dump(list(get_score()), fp, indent=2, sort_keys=True)
