from CloudinaryConfig import config
import cloudinary

cloudinary.config(
cloud_name = config["cloud_name"],
api_key = config["api_key"],
api_secret = config["api_secret"],
api_proxy = config["api_proxy"]
)

import cloudinary.uploader
import cloudinary.api
import requests

import os
import datetime

delete_after = datetime.timedelta(hours = 4)
filepath = "files_to_delete.txt"

def ReadFile(filename):
	f = open(filename)
	all_data = f.readlines()
	f.close()

	publicID_date = []
	for line in all_data:
		line = line.replace("\n", "")
		line = line.split(",")

		time = datetime.datetime.strptime(line[1], '%m-%d-%Y %H:%M:%S')
		publicID_date.append([line[0], time])

	return publicID_date

def WriteFile(filename, data):
	f = open(filename, "w")

	for line in data:
		str_time = line[1].strftime('%m-%d-%Y %H:%M:%S')
		f.write(line[0]+","+str_time+"\n")

	f.close()


def MonitorAndCleanCloud(files_to_delete):
	print(f"Running Cloud Cleaner. Num Files Pending Deletion: {len(files_to_delete)}")
	time_now = datetime.datetime.now()
	objects_to_delete = []
	for file in files_to_delete:
		time_diff = time_now - file[1]

		if time_diff >= delete_after:
			print(f"File {file[0]} will be deleted.")
			objects_to_delete.append(file)

	for obj in objects_to_delete:
		print(f"Deleting {obj[0]}")
		files_to_delete.remove(obj)
		cloudinary.uploader.destroy(obj[0], resource_type = "video")

	return files_to_delete

if __name__ == "__main__":
	files_to_delete = ReadFile(filepath)
	files_to_delete = MonitorAndCleanCloud(files_to_delete)
	WriteFile(filepath, files_to_delete)