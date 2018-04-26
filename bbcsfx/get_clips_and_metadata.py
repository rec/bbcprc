import json, numpy as np, os
from . import audio_io, constants, worker


def write_one_clip(frames, clip_file, seconds=1):
    frame_count = len(frames) / 4
    middle = int(frame_count / 2)

    clip_frame_count = int(seconds * constants.FRAME_RATE)
    half = int(clip_frame_count / 2)

    begin = middle - half
    end = begin + clip_frame_count

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


def metadata_and_clip(filename):
    source_file, metadata_file, clip_file = constants.files(filename)
    metadata_exists = os.path.exists(metadata_file)
    clip_exists = os.path.exists(metadata_file)

    if metadata_file and clip_exists:
        return

    def write_metadata(**md):
        data = json.dumps(md, sort_keys=True)
        try:
            with audio_io.delete_on_fail(metadata_file) as fp:
                fp.write(data)
        except:
            print('Failed to write:', metadata_file)
        else:
            print(filename, '->', data)

    def write_error(*error):
        write_metadata(error=list(error))
        print('ERROR:', filename, *error)

    try:
        frames = audio_io.read_frames(source_file)
    except Exception as e:
        return write_error(repr(e), *e.args)

    if len(frames) % 4:
        return write_error('Frame buffer length must be a multiple of 4')

    if not metadata_exists:
        samples = audio_io.from_frames(frames)
        rms = np.sqrt(np.mean(np.square(samples)))
        write_metadata(frame_count=len(samples), rms=rms)

    if not clip_exists:
        write_one_clip(frames, clip_file)


def get_all():
    files = sorted(os.listdir(constants.SOURCE_DIR))
    worker.work_on(files, metadata_and_clip, PROCESS_COUNT)


PROCESS_COUNT = 4

if __name__ == '__main__':
    get_all()
