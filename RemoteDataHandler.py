import cloudinary

cloudinary.config(
cloud_name = "dpynlgyfi",
api_key = "352343549873159",
api_secret = "t2mYs6FwX5d9ldlSnOqRxFpWWYw"
)

import cloudinary.uploader
import cloudinary.api
import requests


class RemoteDataHandler:
	def __init__(self):
		pass

	def UploadToCloud(self, filepath, resource_type = "video"):
		res = cloudinary.uploader.upload(filepath, folder = "record_data", public_id = "output_record_video", 
										overwrite = True, resource_type = resource_type)

		return res

	def DownloadData(self, url):
		local_filepath = url.split("/")[-1]	

		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filepath, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)	

		return local_filepath