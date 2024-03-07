from flask import Flask, jsonify, request
from flask import Response
import soundfile as sf

from DiskRotation import DiskRotation
from videoMaker import VideoMaker
from RemoteDataHandler import RemoteDataHandler
from YTDownloader import YTDownloader
import datetime
from Mailer import Mailer
import os


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

FILES_DIR = "VIDEO_FILES"

if not os.path.exists(FILES_DIR):
    os.mkdir(FILES_DIR)

YT_DIR = "YOUTUBE_FILES"

if not os.path.exists(YT_DIR):
    os.mkdir(YT_DIR)

WIDTH = 1080
HEIGHT = 1080
DISK_RADIUS = int((min(WIDTH, HEIGHT)/2)*0.8)
FPS = 30

app = Flask(__name__)


@app.route('/generate_video', methods=['POST', "GET"])
def MakeVideo():
    was_YT_mode = False
    data = request.get_json()

    temp_video_filename =  os.path.join(FILES_DIR, data["publicID"]["audio"].replace("/", "_").replace("\\", "_") + "_temp_video.mp4")
    output_video_name =  os.path.join(FILES_DIR, data["publicID"]["audio"].replace("/", "_").replace("\\", "_") + "video.mp4")


    dims = data["dimension"]

    new_width = int(dims.split("x")[0])
    new_height = int(dims.split("x")[1])
    DISK_RADIUS = int((min(new_width, new_height)/2)*0.8)

    DR = DiskRotation(new_width, new_height, disk_radius = DISK_RADIUS, rpm = 225, fps = FPS)
    vid_maker = VideoMaker()
    RDH = RemoteDataHandler()
    mailer = Mailer()
    YT_down = YTDownloader()
    
    audio_file_url = data["audio_file_url"]
    audio_file_url = RDH.DownloadData(audio_file_url, FILES_DIR)

    background_mode = data["backgroundType"]
    
    if background_mode == "color":
        background_image_data = data["background"].lstrip('#')
        color = tuple(int(background_image_data[i:i+2], 16) for i in (0, 2, 4))
        background_image_data = (color[2], color[1], color[0])
    
    elif background_mode == "image":
        background_image_data = data["background"]
        background_image_data = RDH.DownloadData(background_image_data, FILES_DIR)
    
    elif background_mode == "video":
        background_image_data = data["background"]
        background_image_data = RDH.DownloadData(background_image_data, FILES_DIR)
    
    elif background_mode == "youtube":
        background_image_data = data["background"]
        background_image_data = YT_down.DownloadVideo(background_image_data)
        background_mode = "video"
        was_YT_mode = True

    disk_image_data = data["disk_image_url"]
    disk_image_data = RDH.DownloadData(disk_image_data, FILES_DIR)

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

    if background_mode == "video" and not was_YT_mode:
        files_to_delete.append([data["publicID"]["background"], "video"])


    RDH.DeleteFilesNow(files_to_delete)

    time_now = datetime.datetime.now()
    time_now_str = time_now.strftime('%m-%d-%Y %H:%M:%S')

    mailer.SendMail(path["secure_url"], data["email"])
    content = {"out_filename": path["secure_url"]}

    return content, 200


@app.route('/', methods=["GET"])
def AppRoot():
    print("App Root")
    return "Record Maker Root"


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5100)
