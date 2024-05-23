import requests
import random
from RemoteDataHandler import RemoteDataHandler
import time
import sys


RDH = RemoteDataHandler()

def GetImageBGDict(res_audio, res_disk):
	print("Image Background")
	res_Bg =  RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/BG.jpeg", resource_type = "image")
	data = {
	"audio_file_url": res_audio["secure_url"],
	"backgroundType": 'image',
	"background": res_Bg["secure_url"],
	"disk_image_url" : res_disk["secure_url"],
	"watermark" : True,
	"ismember" : False,
	"publicID":{
					"background":res_Bg["public_id"],
					"audio":res_audio["public_id"],
					"center":res_disk["public_id"]
			   },
	"dimension":"1080x1080",
	"email":"zain.9496@gmail.com"
	}

	return data

def GetVideoBGDict(res_audio, res_disk):
	print("Video Background")
	res_Bg =  RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/BG_Vid.mp4", resource_type = "video")
	data = {
	"audio_file_url": res_audio["secure_url"],
	"backgroundType": 'video',
	"background": res_Bg["secure_url"],
	"disk_image_url" : res_disk["secure_url"],
	"watermark" : True,
	"ismember" : False,
	"publicID":{
					"background":res_Bg["public_id"],
					"audio":res_audio["public_id"],
					"center":res_disk["public_id"]
			   },
	"dimension":"1080x1080",
	"email":"zain.9496@gmail.com"
	}

	return data

def GetSolidBGDict(res_audio, res_disk):
	print("Solid Background")
	data = {
	"audio_file_url": res_audio["secure_url"],
	"backgroundType": 'color',
	"background": '#ff0000',
	"disk_image_url" : res_disk["secure_url"],
	"watermark" : True,
	"ismember" : False,
	"publicID":{
					# "background":res_Bg["public_id"],
					"audio":res_audio["public_id"],
					"center":res_disk["public_id"]
			   },
	"dimension":"1080x1080",
	"email":"zain.9496@gmail.com"
	}

	return data

def GetYouTubeBGDict(res_audio, res_disk):
	print("Youtube Background")
	data = {
	"audio_file_url": res_audio["secure_url"],
	"backgroundType": 'youtube',
	"background": 'https://www.youtube.com/watch?v=HVtE2rcJ5yk&ab_channel=MATECA&t=50',
	"disk_image_url" : res_disk["secure_url"],
	"watermark" : True,
	"ismember" : False,
	"publicID":{
					"audio":res_audio["public_id"],
					"center":res_disk["public_id"]
			   },
	"dimension":"1080x1080",
	"email":"zain.9496@gmail.com"
	}

	return data

def TestAll(url):
	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")
	data = GetImageBGDict(res_audio, res_disk)
	resp = requests.get(url, json=data)
	print(resp.text)

	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")
	data = GetVideoBGDict(res_audio, res_disk)
	resp = requests.get(url, json=data)
	print(resp.text)
	
	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")
	data = GetSolidBGDict(res_audio, res_disk)
	resp = requests.get(url, json=data)
	print(resp.text)
	
	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")
	data = GetYouTubeBGDict(res_audio, res_disk)
	resp = requests.get(url, json=data)
	print(resp.text)


def TestAPI():
	print("Starting Test")
	url = "http://3.96.10.95:5100/generate_video"
	# url = "http://192.168.100.20:5100/generate_video"

	if len(sys.argv) > 1:
		test_mode = sys.argv[1].lower()
		
		if test_mode not in ['video', 'image', 'color', 'youtube', 'all']:
			print("valid inputs: video, image, color, youtube and all. Or leave empty to testing image mode.")
			exit()

	else:
		test_mode = "image"


	if test_mode == 'all':
		print("Testing All Modes")
		TestAll(url)
		return
	
	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")


	if test_mode == "image":
		data = GetImageBGDict(res_audio, res_disk)

	elif test_mode == "video":
		data = GetVideoBGDict(res_audio, res_disk)

	elif test_mode == "color":
		data = GetSolidBGDict(res_audio, res_disk)
		
	elif test_mode == "youtube":
		data = GetYouTubeBGDict(res_audio, res_disk)
	
	resp = requests.get(url, json=data)
	print(resp.text)



if __name__ == "__main__":
	TestAPI()