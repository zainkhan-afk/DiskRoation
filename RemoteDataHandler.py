from CloudinaryConfig import config
import cloudinary

cloudinary.config(
cloud_name = config["cloud_name"],
api_key = config["api_key"],
api_secret = config["api_secret"],
api_proxy = config["api_proxy"]
)

import datetime
import cloudinary.uploader
import cloudinary.api
import requests


class RemoteDataHandler:
	def __init__(self, delete_after = datetime.timedelta(minutes = 5)):
		self.files_to_delete = []
		self.delete_after = delete_after

	def UploadToCloud(self, filepath, resource_type = "video"):
		res = cloudinary.uploader.upload(filepath, folder = "dmb_data", 
										overwrite = True, resource_type = resource_type)

		return res

	def DeleteFilesNow(self, publicIDs):
		for obj in publicIDs:
			print(f"Deleting {obj[0]}")
			cloudinary.uploader.destroy(obj[0], resource_type = obj[1])

	def DownloadData(self, url):
		local_filepath = url.split("/")[-1]	

		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filepath, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)	

		return local_filepath


if __name__ == "__main__":
	rdh = RemoteDataHandler()
	rdh.DeleteFilesNow([["record_data/ebirxxebdjjwghzw2nqp", "video"]])