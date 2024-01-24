import moviepy.editor as mp


class VideoMaker:
	def __init__(self):
		pass


	def MakeVideo(self, record_video_name, audio_file_name, output_video_name):
		print("Making final video.")
		audio = mp.AudioFileClip(audio_file_name)
		video = mp.VideoFileClip(record_video_name)
		final = video.set_audio(audio)
		final.write_videofile(output_video_name)


if __name__ == "__main__":
	vm = VideoMaker("video.mp4")
	vm.MakeVideo("video.avi", 'Ed Sheeran - Perfect.mp3')