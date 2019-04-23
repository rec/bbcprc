import json, numpy as np, os
from . import audio_io, constants, files, worker


def write_metadata(filename, md):
    data = json.dumps(md, sort_keys=True)
    metadata_file = constants.metadata(filename)
    try:
        with files.delete_on_fail(metadata_file) as fp:
            fp.write(data)
    except:
        print('Failed to write:', metadata_file)
    else:
        print(filename, '->', data)


def write_one_clip(frames, channels, clip_file, seconds=1):
    frame_size = 2 * channels
    frame_count = len(frames) / frame_size
    middle = int(frame_count / 2)

    clip_frame_count = int(seconds * constants.FRAME_RATE)
    half = int(clip_frame_count / 2)

    begin = (middle - half) * frame_size
    end = begin + clip_frame_count * frame_size

    if 0 < begin < end <= len(frames):
        frames = frames[begin:end]
    else:
        print('Too short!', clip_file, begin, end, len(frames))

    try:
        audio_io.write_frames(clip_file, frames)
    except:
        print('ERROR: clip', clip_file)
    else:
        print('Clip:', clip_file)


def fix_metadata(filename):
    metadata, frames, channels = get_metadata(filename)
    write_metadata(filename, metadata)
    return frames, channels


def get_metadata(filename):
    source_file = constants.source(filename)
    try:
        frames, channels = audio_io.read_frames(source_file)
    except Exception as e:
        return {'error': e.args[0] if e.args else '(none)'}, None, None

    samples = audio_io.from_frames(frames, channels)
    rms = np.sqrt(np.mean(np.square(samples)))
    return {'frame_count': len(samples), 'rms': rms}, frames, channels


def metadata_and_clip(filename):
    if not filename.endswith('.wav'):
        return

    source_file, metadata_file, clip_file = constants.all_files(filename)
    metadata_exists = os.path.exists(metadata_file)
    clip_exists = os.path.exists(clip_file)

    if metadata_file and clip_exists:
        return

    frames, channels = fix_metadata(filename)

    if channels and not clip_exists:
        write_one_clip(frames, channels, clip_file)


if __name__ == '__main__':
    worker.work_on_files(metadata_and_clip, constants.SOURCE_DIR)
