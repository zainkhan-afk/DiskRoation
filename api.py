from flask import Flask, jsonify, request
import soundfile as sf

from DiskRotation import DiskRotation
from videoMaker import VideoMaker
from RemoteDataHandler import RemoteDataHandler
import os

#     "audio_file_url": "",
#     "background_mode": 0,
#     "background_color": (255, 0, 0),
#     "background_image_url": "",
#     "background_video_url": "",
#     "disk_mode" : 0,
#     "disk_color" : 0,
#     "disk_image_url" : "",
#     "watermark" : False

WIDTH = 1080
HEIGHT = 1080
DISK_RADIUS = 300
FPS = 30

vid_maker = VideoMaker()
DR = DiskRotation(WIDTH, HEIGHT, disk_radius = DISK_RADIUS, rpm = 200, fps = FPS)
RDH = RemoteDataHandler()

app = Flask(__name__)


@app.route('/generate_video', methods=['POST', "GET"])
def MakeVideo():
    data = request.get_json()

    temp_video_filename = "temp_video.avi"
    output_video_name = "video.mp4"

    audio_file_url = data["audio_file_url"]
    audio_file_url = RDH.DownloadData(audio_file_url)

    background_mode = data["background_mode"]
    
    if background_mode == 0:
        background_image_data = data["background_color"]
    elif background_mode == 1:
        background_image_data = data["background_image_url"]
        background_image_data = RDH.DownloadData(background_image_data)
    elif background_mode == 2:
        background_image_data = data["background_video_url"]
        background_image_data = RDH.DownloadData(background_image_data)

    disk_mode = data["disk_mode"]
    
    if disk_mode == 0:
        disk_image_data = data["disk_color"]
    elif disk_mode == 1:
        disk_image_data = data["disk_image_url"]
        disk_image_data = RDH.DownloadData(disk_image_data)

    watermark = data["watermark"]

    sound_data, fs = sf.read(audio_file_url, dtype='float32')

    video_time = sound_data.shape[0] / fs


    DR.CreateVideoFrames(video_time, background_mode = background_mode, background_image_data = background_image_data, 
                        disk_mode = disk_mode, disk_image_data = disk_image_data, temp_video_filename = temp_video_filename)
    vid_maker.MakeVideo(temp_video_filename, audio_file_url, output_video_name)

    path = RDH.UploadToCloud(output_video_name, resource_type = "video")


    print("Cleaning Up.")

    os.remove(audio_file_url)
    os.remove(output_video_name)

    if background_mode != 0:
        os.remove(background_image_data)

    if disk_mode != 0:
        os.remove(disk_image_data)

    os.remove(temp_video_filename)


    return {"out_filename": path["secure_url"]}

@app.route('/', methods=["GET"])
def AppRoot():
    print("App Root")
    return "Record Maker Root"

# app.run(host = '0.0.0.0', port = 8501)
app.run()
