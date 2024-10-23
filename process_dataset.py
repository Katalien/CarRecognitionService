import csv
import os
import cv2

class BoundingBox:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

class Sample:
    def __init__(self, image_filepath: str):
        self.image_path = image_filepath
        self.bb_list = []

    def add_bb(self, x_min: float, y_min: float, x_max: float, y_max: float):
        self.bb_list.append(BoundingBox(x_min, y_min, x_max, y_max))

dataset_path = "./data/"
images_path = f"{dataset_path}images/"
labels_csv_path = f"{dataset_path}labels.csv"
save_path = "./data/labeled_samples/"


samples_dict = {}
with open(labels_csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i, row in enumerate(spamreader):
        if i == 0:
            continue
        row = ', '.join(row)
        row_items = row.split(',')
        image_path = os.path.join(images_path, row_items[0])
        if image_path in samples_dict:
            sample = samples_dict[image_path]
        else:
            sample = Sample(image_filepath=image_path)

        sample.add_bb(x_min=float(row_items[1]),
                      y_min=float(row_items[2]),
                      x_max=float(row_items[3]),
                      y_max=float(row_items[4]))
        samples_dict[image_path] = sample

for path, sample in samples_dict.items():
    print(path, len(sample.bb_list))
    image_path = sample.image_path
    image = cv2.imread(image_path)
    for bb in sample.bb_list:
        image = cv2.rectangle(image, (int(bb.x_min), int(bb.y_min)),
                              (int(bb.x_max), int(bb.y_max)), (0, 0, 255), 1)
    cv2.imwrite(f"{save_path}{sample.image_path.split('/')[-1]}", image)

