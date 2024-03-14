import os
import youtube_dl

class YTDownloader:
	def __init__(self, YT_dir, desired_height = 1080, desired_extension = "mp4"):
		self.YT_dir = YT_dir
		self.desired_height = desired_height
		self.desired_extension = desired_extension


	def GetDownloadOptions(self, formats, title, audioPublicID):
		options = {}

		diff = 10000
		closest_height = 0
		extension = ""

		filename = title + "_" + audioPublicID

		for f in formats:
			if 'height' in f:
				if f['height'] == self.desired_height and f["ext"] == self.desired_extension: 
					extension = self.desired_extension
					closest_height = self.desired_height
					break

				elif f['height'] == self.desired_height and f["ext"] != self.desired_extension:
					closest_height = self.desired_height
					extension = f["ext"]
					
				if closest_height != self.desired_height:
					if abs(f['height'] - self.desired_height) < diff:
						diff = abs(f['height'] - self.desired_height)
						closest_height = f['height']
						extension = f["ext"]


		filename += f".{extension}"
		options = {
						"format" : f"{extension}[height={closest_height}]",
						"outtmpl": f'{self.YT_dir}/%(title)s_{audioPublicID}.%(ext)s'
				  }

		return options, os.path.join(self.YT_dir, filename)

	def DownloadVideo(self, url, audioPublicID):
		ydl_opts = {}
		ydl = youtube_dl.YoutubeDL(ydl_opts)

		info_dict = ydl.extract_info(url, download=False)

		title = info_dict.get("title", None)

		formats = info_dict.get('formats',None)

		ydl_opts, filepath = self.GetDownloadOptions(formats, title, audioPublicID)

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])

		return filepath


if __name__ == "__main__":
	url = "https://www.youtube.com/watch?v=vJ6T7bV6Zo0"

	yt_down = YTDownloader("YOUTUBE_FILES", desired_height = 720)
	filepath = yt_down.DownloadVideo(url, "32123123")

	print(filepath)

	# import cv2

	# cap = cv2.VideoCapture(filepath)

	# while True:
	# 	ret, frame = cap.read()

	# 	if not ret:
	# 		break

	# 	print(frame.shape)