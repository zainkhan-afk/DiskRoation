import requests
import random

# data = {
# "audio_file_url": "https://res.cloudinary.com/dpynlgyfi/video/upload/v1706090865/record_data/audio.mp3",
# "backgroundType": 'color,image,video',
# "background": 'imgurl,videourl,color',
# "disk_image_url" : "https://res.cloudinary.com/dpynlgyfi/image/upload/v1706090889/record_data/IM.jpg",
# "watermark" : False,
# "publicID":{
# 				"background":"public_Id",
# 				"audio":"public_id",
# 				"center":"public_id"
# 		   },
# "dimension":"1080x1080,1920x1080",
# "email":"user email"
# }


# "background_image_url": "https://res.cloudinary.com/dpynlgyfi/image/upload/v1706090889/record_data/JB.jpg",
# "background_video_url": "https://res.cloudinary.com/dpynlgyfi/video/upload/v1706090892/record_data/BG_vid.mp4",

data = {
"audio_file_url": "https://res.cloudinary.com/dpynlgyfi/video/upload/v1706090865/record_data/audio.mp3",
"backgroundType": 'video',
"background": "https://res.cloudinary.com/dpynlgyfi/video/upload/v1706090892/record_data/BG_vid.mp4",
"disk_image_url" : "https://res.cloudinary.com/dpynlgyfi/image/upload/v1706090889/record_data/IM.jpg",
"watermark" : True,
"publicID":{
				"background":f"{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}",
				"audio":f"{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}",
				"center":f"{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}"
		   },
"dimension":"1080x1080",
"email":"user email"
}


url = "https://zainkhan.pythonanywhere.com/generate_video"
# url = "http://127.0.0.1:5000/generate_video"

resp = requests.get(url, json=data)
print(resp.json())