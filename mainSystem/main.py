import os
import sys
sys.path.append('.')
import configparser
import time
from mainSystem.processSingleCamera import singleCameraProcessor


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

    for oneSection in cf.sections():
        if "camera" in oneSection:
            inputStream = cf.get(oneSection, "input_stream")
            cameraID = cf.get(oneSection, "camera_id")
            print('inputStream:', inputStream)
            processors.append(singleCameraProcessor(cf, inputStream, cameraID))

    for oneWork in processors:
        oneWork.start()

    while True:
        for index, oneWork in enumerate(processors):
            if not oneWork.is_alive():
                processors[index] = singleCameraProcessor(cf, oneWork.inputStream, oneWork.cameraID)
                processors[index].start()
            time.sleep(1)
