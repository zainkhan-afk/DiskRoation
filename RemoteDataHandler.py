import cloudinary
import datetime

cloudinary.config(
cloud_name = "dpynlgyfi",
api_key = "352343549873159",
api_secret = "t2mYs6FwX5d9ldlSnOqRxFpWWYw",
# api_proxy = "http://proxy.server:3128"
)

import cloudinary.uploader
import cloudinary.api
import requests


class RemoteDataHandler:
	def __init__(self, delete_after = datetime.timedelta(minutes = 5)):
		self.files_to_delete = []
		self.delete_after = delete_after

	def UploadToCloud(self, filepath, public_ID, resource_type = "video"):
		res = cloudinary.uploader.upload(filepath, folder = "record_data", public_id = public_ID, 
										overwrite = True, resource_type = resource_type)

		return res

	def DownloadData(self, url, public_ID):
		local_filepath = public_ID + "_" + url.split("/")[-1]	

		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filepath, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)	

		return local_filepath