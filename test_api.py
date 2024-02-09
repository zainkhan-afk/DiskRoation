import requests
import random
from RemoteDataHandler import RemoteDataHandler


def TestAPI():
	print("Starting Test")
	RDH = RemoteDataHandler()

	res_audio = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/audio.mp3", resource_type = "video")
	res_Bg =  RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/BG.jpeg", resource_type = "image")
	res_disk = RDH.UploadToCloud("D:/zain_dev/python_dev/rotating_disk/data/disk.jpg", resource_type = "image")

	data = {
	"audio_file_url": res_audio["secure_url"],
	"backgroundType": 'image',
	"background": res_Bg["secure_url"],
	"disk_image_url" : res_disk["secure_url"],
	"watermark" : True,
	"publicID":{
					"background":res_Bg["public_id"],
					"audio":res_audio["public_id"],
					"center":res_disk["public_id"]
			   },
	"dimension":"1080x1080",
	"email":"zain.9496@gmail.com"
	}

	# data =  {
	# "audio_file_url": "https://res.cloudinary.com/df7gif899/video/upload/v1707162063/audioshit/d42immutj7m1zwiufzmf.mp3",
	# "publicID": {
	# "center": "backroundmb/ej6uwpm2mlatinymckrj",
	# "audio": "audioshit/d42immutj7m1zwiufzmf",
	# "background": "backroundmb/pxf7d5okzhqfor0ikjmh"
	# },
	# "background": "https://res.cloudinary.com/df7gif899/image/upload/c_thumb,w_1080,h_1080/v1707162063/backroundmb/pxf7d5okzhqfor0ikjmh.jpg",
	# "backgroundType": "image",
	# "disk_image_url": "https://res.cloudinary.com/df7gif899/image/upload/c_thumb,w_700,h_700/v1707162059/backroundmb/ej6uwpm2mlatinymckrj.png",
	# "dimension": "1080x1080",
	# "watermark": True,
	# "email": "muhammadmoiz2194@gmail.com"
	# }


	# url = "http://15.156.71.130:5100/generate_video"
	url = "http://127.0.0.1:5100/generate_video"

	print("Sending Request")
	resp = requests.get(url, json=data)
	print(resp.text)
	print(resp.json())

if __name__ == "__main__":
	TestAPI()