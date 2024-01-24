import cv2
import numpy as np


class DiskRotation:
	def __init__(self, width, height, disk_radius = 400, rpm = 60, fps = 30):
		self.Reset(width, height, disk_radius, rpm, fps)

	def Reset(self, width, height, disk_radius = 400, rpm = 60, fps = 30):
		self.width = width
		self.height = height
		self.disk_radius = disk_radius
		self.rpm = rpm
		self.fps = fps

		self.radians_per_second = self.rpm*2*np.pi / 60

		self.disk_mask = np.zeros((self.height, self.width, 3)).astype("uint8")
		cv2.circle(self.disk_mask, (self.width // 2, self.height // 2), self.disk_radius, (255, 255, 255), -1)

		self.disk_mask = self.disk_mask.astype("float32") / 255


		self.Clear()


	def FormatImage(self, image, new_width, clip_height_to):
		H, W, _ = image.shape
		new_W = new_width
		new_H = int(new_W * H / W)

		image = cv2.resize(image, (new_W, new_H))

		if new_H > clip_height_to:
			diff = new_H - clip_height_to
			crop_x1 = 0
			crop_x2 = new_W
			crop_y1 = diff // 2
			crop_y2 = diff // 2 + clip_height_to

			image = image[crop_y1:crop_y2, crop_x1:crop_x2]

		if new_H < clip_height_to:
				diff = clip_height_to - new_H

				crop_x1 = 0
				crop_x2 = new_W
				crop_y1 = diff // 2
				crop_y2 = diff // 2 + new_H

				new_image = np.zeros((new_width, clip_height_to, 3)).astype("uint8")
				new_image[crop_y1:crop_y2, crop_x1:crop_x2] = image
				image = new_image.copy()

		return image

	def LoadVideoImages(self, video_path):
		cap = cv2.VideoCapture(video_path)
		all_video_frames = []
		while True:
			ret, img = cap.read()
			if not ret:
				break
			img = self.FormatImage(img, new_width = self.width, clip_height_to = self.height)
			all_video_frames.append(img)

		return all_video_frames

	def DrawDisk(self, disk_image, background_image, t):
		angle = -t*self.radians_per_second
		disk = self.RotateImage(disk_image.copy(), angle)

		h, w, _ = self.frame.shape
		disk_h, disk_w, _ = disk.shape

		disk_x1 = w // 2 - disk_w // 2
		disk_y1 = h // 2 - disk_h // 2

		disk_x2 = w // 2 + disk_w // 2
		disk_y2 = h // 2 + disk_h // 2


		disk_frame = np.zeros((self.height, self.width, 3)).astype("uint8")
		disk_frame[disk_y1:disk_y2, disk_x1:disk_x2] = disk
		disk_frame = disk_frame.astype("float32") / 255

		background_frame = background_image.copy().astype("float32") / 255



		self.frame = ((background_frame*(1 - self.disk_mask) + disk_frame*self.disk_mask)*255).astype("uint8")

	def RotateImage(self, image, angle):
	    row, col = image.shape[:2]
	    center = tuple(np.array([row,col])/2)
	    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
	    new_image = cv2.warpAffine(image, rot_mat, (col, row))
	    return new_image

	def Clear(self):
		self.frame = np.zeros((self.height, self.width, 3))


	def CreateVideoFrames(self, time, background_mode = 0, background_image_data = None, disk_mode = 0, disk_image_data = None,  temp_video_filename = "video_temp.avi"):
		if background_mode not in [0, 1, 2]:
			print("Background mode is invalid. Must be 0, 1 or 2.")
			return False

		if disk_mode not in [0, 1]:
			print("Disk mode is invalid. Must be 0 or 1.")
			return False

		all_background_frames = None
		bg_image = None
		disk_image = None
		if background_mode == 0:
			bg_image = np.zeros((self.height, self.width, 3)).astype("uint8")
			bg_image[:, :, 0] = background_image_data[0]
			bg_image[:, :, 1] = background_image_data[1]
			bg_image[:, :, 2] = background_image_data[2]

		elif background_mode == 1:
			bg_image = cv2.imread(background_image_data)
			bg_image = self.FormatImage(bg_image, new_width = self.width, clip_height_to = self.height)

		elif background_mode == 2:
			all_background_frames = self.LoadVideoImages(background_image_data)


		if disk_mode == 0:
			disk_image = np.zeros((self.disk_radius*2, self.disk_radius*2, 3)).astype("uint8")
			disk_image[:, :, 0] = disk_image_data[0]
			disk_image[:, :, 1] = disk_image_data[1]
			disk_image[:, :, 2] = disk_image_data[2]

		elif disk_mode == 1:
			disk_image = cv2.imread(disk_image_data)
			disk_image = self.FormatImage(disk_image, new_width = self.disk_radius*2, clip_height_to = self.disk_radius*2)



		num_frames = int(time*self.fps)
		delta_t = 1 / self.fps


		size = (self.width, self.height)
		writer = cv2.VideoWriter(temp_video_filename,  cv2.VideoWriter_fourcc(*'MJPG'), self.fps, size) 



		bg_img_idx = 0
		t = 0
		for i in range(num_frames):
			if i % 1000 == 0:
				print(f"{i} / {num_frames} completed")

			self.Clear()


			if background_mode == 2:
				bg_image = all_background_frames[bg_img_idx]
				bg_img_idx += 1

				if bg_img_idx>=len(all_background_frames):
					bg_img_idx = 0

			self.DrawDisk(disk_image, bg_image, t)
			writer.write(self.frame)

			# cv2.imshow("F", self.frame)
			# k = cv2.waitKey(1)

			# if k == ord("q"):
			# 	break

			t += delta_t


		writer.release()
		return True