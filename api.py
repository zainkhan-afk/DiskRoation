from flask import Flask, jsonify, request
import soundfile as sf

from DiskRotation import DiskRotation
from videoMaker import VideoMaker
from RemoteDataHandler import RemoteDataHandler
import os
import datetime


# "audio_file_url": "https://res.cloudinary.com/dpynlgyfi/video/upload/v1706090865/record_data/audio.mp3",
# "backgroundType": 'color,image,video',
# "background": 'imgurl,videourl,color',
# "disk_image_url" : "https://res.cloudinary.com/dpynlgyfi/image/upload/v1706090889/record_data/IM.jpg",
# "watermark" : False,
# "publicID":{
#               "background":"public_Id",
#               "audio":"public_id",
#               "center":"public_id"
#          },
# "dimension":"1080x1080,1920x1080",
# "email":"user email"

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
    files_to_delete_path = "files_to_delete.txt"

    if not os.path.exists(files_to_delete_path):
        f = open(files_to_delete_path, "w")
        f.close()


    data = request.get_json()

    temp_video_filename =  "temp_video.avi"
    output_video_name =  "video.mp4"

    dims = data["dimension"]

    new_width = int(dims.split("x")[0])
    new_height = int(dims.split("x")[1])
    DR.SetSize(new_width, new_height)

    audio_file_url = data["audio_file_url"]
    audio_file_url = RDH.DownloadData(audio_file_url)

    background_mode = data["backgroundType"]
    
    if background_mode == "color":
        background_image_data = data["background"]
    elif background_mode == "image":
        background_image_data = data["background"]
        background_image_data = RDH.DownloadData(background_image_data)
    elif background_mode == "video":
        background_image_data = data["background"]
        background_image_data = RDH.DownloadData(background_image_data)

    disk_image_data = data["disk_image_url"]
    disk_image_data = RDH.DownloadData(disk_image_data)

    watermark = data["watermark"]

    sound_data, fs = sf.read(audio_file_url, dtype='float32')

    video_time = sound_data.shape[0] / fs


    DR.CreateVideoFrames(video_time, use_watermark = watermark, background_mode = background_mode, background_image_data = background_image_data, 
                        disk_image_data = disk_image_data, temp_video_filename = temp_video_filename)
    vid_maker.MakeVideo(temp_video_filename, audio_file_url, output_video_name)


    path = RDH.UploadToCloud(output_video_name, resource_type = "video")
    
    print("Cleaning Up.")

    os.remove(audio_file_url)

    if background_mode != "color":
        os.remove(background_image_data)

    os.remove(disk_image_data)
    os.remove(temp_video_filename)
    os.remove(output_video_name)

    files_to_delete = [[data["publicID"]["audio"], "video"]]
    files_to_delete.append([data["publicID"]["center"], "image"])

    if background_mode == "image":
        files_to_delete.append([data["publicID"]["background"], "image"])

    if background_mode == "video":
        files_to_delete.append([data["publicID"]["background"], "video"])


    RDH.DeleteFilesNow(files_to_delete)

    time_now = datetime.datetime.now()
    time_now_str = time_now.strftime('%m-%d-%Y %H:%M:%S')

    f = open(files_to_delete_path, "a")
    f.write(path["public_id"] + "," + time_now_str + "\n")
    f.close()

    print(path)

    return {"out_filename": path["secure_url"]}

@app.route('/', methods=["GET"])
def AppRoot():
    print("App Root")
    return "Record Maker Root"



app.run(host = '0.0.0.0', port = 5100)
