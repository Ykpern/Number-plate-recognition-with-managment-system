import numpy as np
from ultralytics import YOLO
import cv2
import timeit
from LPQuerys import entranceLog, check

#from sort.sort import *
from util import read_license_plate, write_csv, convol

results = {}
#mot_tracker = Sort()

kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

coco_model = YOLO('./yolov8n.pt')
license_plate_detector = YOLO('./license_plate_detector.pt')

cap = cv2.VideoCapture(0)
duration = cap.get(cv2.CAP_PROP_POS_MSEC)
fps = cap.get(cv2.CAP_PROP_FPS)

vehicles = [2, 3, 5, 7]

frame_nmr = -1
ret = True
car_id = -1
license_score_max = 0

licence_plate_prev = ''
while ret:
    ret, frame = cap.read()
    frame_nmr += 1
    start = timeit.default_timer()

    if ret and frame_nmr % fps == 0:
        results[frame_nmr] = {}

        #detect vehicle
        detections = coco_model(frame)[0]
        detections_ = []

        for detection in detections.boxes.data.tolist():
            #print(detection)
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        #track vehicles

        #track_ids = mot_tracker.update(np.asarray(detections_))

        #detect plates
        license_plates = license_plate_detector(frame)[0]

        for license_plate in license_plates.boxes.data.tolist():
            # print(detection)
            x1, y1, x2, y2, score, class_id = license_plate
            #l,cense plate 2 caar assign
            #xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate) #,track_ids)
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), ]

            # proocess license plate

            license_plate_crop_sharp = cv2.filter2D(license_plate_crop, -1, kernel)
            #license_plate_crop_sharp = cv2.GaussianBlur(license_plate_crop, (5,5), 1)

            """cv2.imshow('License Plate Crop sharp', license_plate_crop_sharp)"""


            """(row, col) = license_plate_crop.shape[0:2]
            license_plate_crop_gray = np.zeros([row, col])

            for i in range(row):
                for j in range(col):
                    # Find the average of the BGR pixel values
                    sum = int(license_plate_crop[i, j, 0] * 0.299 + license_plate_crop[i, j, 1] * 0.5870 + \
                              license_plate_crop[i, j, 2] * 0.1140)  #Y' = 0.2989 R + 0.5870 G + 0.1140 B

                    license_plate_crop_gray[i, j] = sum"""


            License_plate_crop_gray = cv2.cvtColor(license_plate_crop_sharp, cv2.COLOR_BGR2GRAY)

            #License_plate_crop_gray_blur = cv2.GaussianBlur(License_plate_crop_gray, (5,5), 1)
            #license_plate_crop_sharp = convol(license_plate_crop_gray, kernel)

            #license_plate_crop_sharp = (license_plate_crop_sharp).astype(np.uint8)
            # change gray image to 8 bit grayscale

            license_plate_crop_gray_equ = cv2.equalizeHist(License_plate_crop_gray)

            _, license_plate_crop_THRESH = cv2.threshold(license_plate_crop_gray_equ, 100, 255, cv2.THRESH_BINARY_INV)

            """cv2.imshow('License Plate Crop sharp', license_plate_crop_THRESH)
            cv2.imshow('License Plate Crop1', license_plate_crop_gray_equ)
            #cv2.imshow('License Plate Crop2', license_plate_crop_gray_equ)
            cv2.imshow('license_plate_crop3', license_plate_crop_THRESH)"""

            #cv2.waitKey(0)

            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_THRESH)

            if license_plate_text is not None and license_plate_text_score > license_score_max:
                license_score_max = license_plate_text_score
                results[frame_nmr][car_id] = {'car': {},
                                              'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                'text': license_plate_text,
                                                                'bbox_score': score,
                                                                'text_score': license_plate_text_score}}
            if frame_nmr % fps*10 == 0:
                if (licence_plate_prev != license_plate_text):
                    license_score_max = 0
                    licence_plate_prev = license_plate_text
                    write_csv(results, './test.csv')



                    if (check(license_plate_text)):
                        success, LPdb = cv2.imencode('.jpg', license_plate_crop)
                        LPdb = LPdb.tobytes()
                        entranceLog(license_plate_text, LPdb)
                        stop = timeit.default_timer()
                        print('Time: ', stop - start, frame_nmr)
                    else:
                        stop = timeit.default_timer()
                        print('Time: ', stop - start, frame_nmr)
                        # print('Time: ', stop - start, frame_nmr)
                        # else() alert security
                else:
                    print('Time: ', stop - start, frame_nmr)



            car_id = car_id + 1

#results
