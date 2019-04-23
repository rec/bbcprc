import math


def run():
    min_frames, log_sum, lines = 0, 0, 0
    for line in open('/tmp/results.txt'):
        try:
            i, f, t, f = line.strip().split()
        except:
            print('Failed to read line', line.strip())
        frames = int(f.strip())
        min_frames = min_frames or frames
        log = 1 + math.log2(frames / min_frames)
        log_sum += log
        lines += 1

    print(log_sum, lines, log_sum / lines)



if __name__ == '__main__':
    run()
