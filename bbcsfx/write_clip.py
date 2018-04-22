import os
from . import constants, to_npy


def write_clip(filename, seconds=1):
    clip_file = os.path.join(constants.CLIP_DIR, filename)
    if os.path.exists(clip_file):
        return

    wave_file = os.path.join(constants.OUTPUT_DIR, filename)
    frames = to_npy.read_frames(wave_file)

    assert 0 == len(frames) % 4, 'Frame buffer not multiple of 4'

    frame_count = len(frames) / 4
    middle = int(frame_count / 2)

    clip_frame_count = int(seconds * constants.SAMPLE_RATE)
    half = int(clip_frame_count / 2)

    begin = middle - half
    end = start + clip_frame_count

    if 0 < begin < end <= len(frames):
        frames = frames[begin:end]
    else:
        print('Too short!', filename, begin, end, len(frames))

    to_npy.write_frames(clip_file, frames)
