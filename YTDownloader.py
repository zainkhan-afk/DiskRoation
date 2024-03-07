import os
import youtube_dl

class YTDownloader:
	def __init__(self, YT_dir, desired_height = 1080, desired_extension = "mp4"):
		self.YT_dir = YT_dir
		self.desired_height = desired_height
		self.desired_extension = desired_extension


	def GetDownloadOptions(self, formats, title):
		options = {}

		diff = 10000
		closest_height = 0
		extension = ""

		filename = title

		for f in formats:
			if 'height' in f:
				if f['height'] == self.desired_height and f["ext"] == self.desired_extension: 
					extension = self.desired_extension
					closest_height = self.desired_height
					filename = f"{title}.{f['ext']}"
					break

				elif f['height'] == self.desired_height and f["ext"] != self.desired_extension:
					closest_height = self.desired_height
					extension = f["ext"]
					filename += f".{f['ext']}"
					break
					
				else:
					if abs(f['height'] - self.desired_height) < diff:
						diff = abs(f['height'] - self.desired_height)
						closest_height = f['height']
						extension = f["ext"]
						filename += f".{f['ext']}"




		options = {
						"format" : f"{extension}[height={closest_height}]",
						"outtmpl": f'{self.YT_dir}/%(title)s.%(ext)s'
				  }

		return options, os.path.join(self.YT_dir, filename)

	def DownloadVideo(self, url):
		ydl_opts = {}
		ydl = youtube_dl.YoutubeDL(ydl_opts)

		info_dict = ydl.extract_info(url, download=False)

		title = info_dict.get("title", None)

		formats = info_dict.get('formats',None)

		ydl_opts, filepath = self.GetDownloadOptions(formats, title)

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])

		return filepath


if __name__ == "__main__":
	url = "https://www.youtube.com/watch?v=HVtE2rcJ5yk&ab_channel=MATECA"

	yt_down = YTDownloader("YOUTUBE_FILES", desired_height = 720)
	yt_down.DownloadVideo(url)