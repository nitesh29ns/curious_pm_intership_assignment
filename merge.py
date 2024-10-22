from moviepy.editor import *
import ffmpeg


def merge_video_audio(input_video:str, input_audio:str):
    try:

        video = ffmpeg.input(input_video) #"D:\ml\curious-pm-poc\code-samples-for-poc-streamlit\sample.mp4

        audio = ffmpeg.input(input_audio) #"D:\ml\curious-pm-poc\code-samples-for-poc-streamlit\output.mp3"

        ffmpeg.concat(video, audio, v=1, a=1).output('./finished_video.mp4').run(overwrite_output=True)

        return "./finished_video.mp4"

    except Exception as e:
        raise e


