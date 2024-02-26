import moviepy.editor as mp


class VideoMaker:
	def __init__(self):
		pass


	def MakeVideo(self, record_video_name, audio_file_name, output_video_name):
		print("Making final video.")
		audio = mp.AudioFileClip(audio_file_name)
		video = mp.VideoFileClip(record_video_name)
		final = video.set_audio(audio)
		final.write_videofile(output_video_name, audio_codec = "aac")
