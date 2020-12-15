import os
import sys
sys.path.append('.')
import configparser
import time
from main_2015.processSingleCamera import singleCameraProcessor
import multiprocessing
from flask import Response
from flask import Flask, jsonify
from flask import render_template
import threading
import cv2
import json

# initialize the output frame and a lock used to ensure thread-safe exchanges of the output frames 
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

def production(q):
    # grab global references to the video stream, output frame, and lock variables
    global outputFrame, lock
    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it, convert the frame to grayscale, and blur it
        # frame = videostream.read()
        frame = q.get()
        print('size:', frame.shape)

        # cv2.imshow('production', frame)
        # cv2.waitKey(0)
        # acquire the lock, set the output frame, and release the lock
        with lock:
            outputFrame = frame.copy()
        
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media type (mime type)
    return Response(generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/show")
def show():
    if os.path.exists("./main_2015/intrusion.json"):
        with open("./main_2015/intrusion.json", "r", encoding='utf8') as f:
            json_datas = json.load(f)
    else:
        json_datas = {}
    return jsonify(json_datas)

if __name__ == "__main__":
    cwd = os.getcwd()
    configFile = os.path.join(cwd, "./config/config.ini")
    if not os.path.join(configFile):
        print("config file isn't exist")
        exit(1)
    print(configFile)
    cf = configparser.ConfigParser()
    cf.read(configFile, encoding="utf-8")

    processors = []
    mgr = multiprocessing.Manager()
    identityBase = mgr.dict()
    identityBase['nextId'] = 0
    q = mgr.Queue(maxsize=27)

    for oneSection in cf.sections():
        if "camera" in oneSection:
            inputStream = cf.get(oneSection, "input_stream")
            cameraID = cf.get(oneSection, "camera_id")
            print('inputStream:', inputStream)
            sc = singleCameraProcessor(cf, inputStream, cameraID, identityBase, q)
            processors.append(sc)
    sc.start()
    # for oneWork in processors:
    #     oneWork.start()

    time.sleep(10)
    # ======================
    # start a thread that will perform motion detection
    t = threading.Thread(target=production, args=(q,))
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=8000, debug=True,
          threaded=True, use_reloader=False)
    # ======================


    while True:
        time.sleep(100)
        # for index, oneWork in enumerate(processors):
        #     if not oneWork.is_alive():
        #         processors[index] = singleCameraProcessor(cf, oneWork.inputStream, oneWork.cameraID, identityBase)
        #         processors[index].start()
        #     time.sleep(1)
