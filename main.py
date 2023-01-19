import random
from ast import literal_eval

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from skimage import io

RANDOM_IMAGE = random.randint(0, 25000)  # random image to show with drawn bounding box

counter = 0
annotations = dict()
ignore_list = []
for csv_file in ['og_dataset/retail50k_train_1.csv', 'og_dataset/retail50k_train_2.csv']:
    train_csv_file = pd.read_csv(csv_file)
    image_links, polygons = train_csv_file['ImageUrl'], train_csv_file['Polygon']
    counter = 0
    for link, polygon in zip(image_links, polygons):
        polygon = literal_eval(polygon)
        # discard weirdly annotated polygons
        if len(polygon) != 4 \
                or polygon[0][0] > 1 \
                or polygon[0][1] > 1 \
                or polygon[1][0] > 1 \
                or polygon[1][1] > 1 \
                or polygon[2][0] > 1 \
                or polygon[2][1] > 1 \
                or polygon[3][0] > 1 \
                or polygon[3][1] > 1 \
                or polygon[0][0] < 0 \
                or polygon[0][1] < 0 \
                or polygon[1][0] < 0 \
                or polygon[1][1] < 0 \
                or polygon[2][0] < 0 \
                or polygon[2][1] < 0 \
                or polygon[3][0] < 0 \
                or polygon[3][1] < 0:
            continue

        if counter == RANDOM_IMAGE:
            # prikazi random primjer s iscrtanim pravokutnikom
            img_array = io.imread(link)
            img = Image.fromarray(img_array, 'RGB')
            width, height = img_array.shape[1], img_array.shape[0]

            # vrhovi poligona
            x00 = polygon[0][0]
            x01 = polygon[0][1]
            x10 = polygon[1][0]
            x11 = polygon[1][1]
            x20 = polygon[2][0]
            x21 = polygon[2][1]
            x30 = polygon[3][0]
            x31 = polygon[3][1]

            # draw points
            # img_array[int(x01 * height) - 1][int(x00 * width) - 1] = [255, 0, 0]
            # img_array[int(x11 * height) - 1][int(x10 * width) - 1] = [255, 0, 0]
            # img_array[int(x21 * height) - 1][int(x20 * width) - 1] = [255, 0, 0]
            # img_array[int(x31 * height) - 1][int(x30 * width) - 1] = [255, 0, 0]

            # working with integers
            # rect = cv2.minAreaRect(np.array([[int(x00 * width), int(x01 * height)],
            #                                  [int(x10 * width), int(x11 * height)],
            #                                  [int(x20 * width), int(x21 * height)],
            #                                  [int(x30 * width), int(x31 * height)]], np.int0))

            rect = cv2.minAreaRect(np.array([[x00 * width, x01 * height],
                                             [x10 * width, x11 * height],
                                             [x20 * width, x21 * height],
                                             [x30 * width, x31 * height]], np.float32))
            angle = rect[2]
            # print(angle)

            bounding_box = cv2.boxPoints(rect)
            bounding_box = np.int0(bounding_box)
            cv2.drawContours(img_array, [bounding_box], 0, (255, 0, 0), 2)

            imgToDisplay = Image.fromarray(img_array, 'RGB')
            imgToDisplay.show()
            print()

        # <X center> <Y center> <Box width> <Box height>
        # vrhovi poligona
        x00 = polygon[0][0]
        x01 = polygon[0][1]
        x10 = polygon[1][0]
        x11 = polygon[1][1]
        x20 = polygon[2][0]
        x21 = polygon[2][1]
        x30 = polygon[3][0]
        x31 = polygon[3][1]

        rect = cv2.minAreaRect(np.array([[x00, x01],
                                         [x10, x11],
                                         [x20, x21],
                                         [x30, x31]], np.float32))
        angle = rect[2]
        if counter == RANDOM_IMAGE:
            print(angle)

        if abs(angle) <= 1 or abs(angle) >= 89:
            if counter == RANDOM_IMAGE:
                print("accepted!")
            if link not in ignore_list:
                if abs(angle) >= 89:
                    annotations[link] = annotations.get(link, []) + [
                        "0 " + str(rect[0][0]) + " " + str(rect[0][1]) + " " + str(rect[1][1]) + " " + str(rect[1][0])]
                elif abs(angle) <= 1:
                    annotations[link] = annotations.get(link, []) + [
                        "0 " + str(rect[0][0]) + " " + str(rect[0][1]) + " " + str(rect[1][0]) + " " + str(rect[1][1])]
        else:
            ignore_list.append(link)
            annotations.pop(link, None)
        counter += 1

print(len(annotations))
with open("train_links.txt", 'w') as f:
    [f.write(photo_url + '\n') for photo_url in annotations.keys()]
with open("train_annotations.txt", 'w') as f:
    for photo_url_list in annotations.values():
        for photo_url in photo_url_list:
            f.write(photo_url + ' - ')
        f.write('\n')
