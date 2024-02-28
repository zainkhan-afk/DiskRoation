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
# filepath = "files_to_delete.txt"

def GetFilesToDelete():
	# 2024-02-12T15:49:17+00:00
	files_to_delete = []
	results = cloudinary.Search().expression("dmb_data/*").execute()
	time_now = datetime.datetime.now()
	for result in results["resources"]:
		date = result["created_at"].split("+")[0]
		time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

		time_diff = time_now - time

		if time_diff >= delete_after:
			files_to_delete.append(result["public_id"])

	return files_to_delete


def DeleteFromCloud(files_to_delete):
	num_deleted = 0
	res = cloudinary.api.delete_resources(files_to_delete, resource_type="video", type="upload")
	
	for f in res["deleted"]:
		if res["deleted"][f] == 'deleted':
			num_deleted += 1

	return num_deleted


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
	# files_to_delete = ReadFile(filepath)
	# files_to_delete = MonitorAndCleanCloud(files_to_delete)
	# WriteFile(filepath, files_to_delete)

	# results = cloudinary.Search().expression("dmb_data/*").execute()
	# for result in results["resources"]:
	# 	print(result["created_at"], result["public_id"])


	files_to_delete = GetFilesToDelete()
	print(f"Files selected to be deleted: {len(files_to_delete)}")
	if len(files_to_delete) != 0:
			num_deleted = DeleteFromCloud(files_to_delete)
			print(f"Files delted: {num_deleted}")