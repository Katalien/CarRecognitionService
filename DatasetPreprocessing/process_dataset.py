import csv
import os
import cv2
import random
from DatasetPreprocessing import Sample

def get_all_samples(label_csv_path):
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
                sample = Sample.Sample(image_filepath=image_path)

            sample.add_bb(x_min=float(row_items[1]),
                          y_min=float(row_items[2]),
                          x_max=float(row_items[3]),
                          y_max=float(row_items[4]))
            samples_dict[image_path] = sample
    return samples_dict


def normalize_coordinate(value, dimension):
    return value / dimension

def convert2orig_coordinates(value, dimension):
    return value * dimension

def convert_coordinates(min_point, max_point, height, width):
    x_center = (min_point[0] + max_point[0]) / 2
    y_center = (min_point[1] + max_point[1]) / 2
    box_width = max_point[0] - min_point[0]
    box_height = max_point[1] - min_point[1]

    x_center_normal = normalize_coordinate(x_center, width)
    y_center_normal = normalize_coordinate(y_center, height)
    box_width_normal = normalize_coordinate(box_width, width)
    box_height_normal = normalize_coordinate(box_height, height)
    return x_center_normal, y_center_normal, box_height_normal, box_width_normal

def convert2yolo_format(samples_dict, save_path):
    class_label = "0"
    for path, sample in samples_dict.items():
        print(path, len(sample.bb_list))
        image_name = sample.image_path.split("/")[-1].split(".")[0]
        image_path = sample.image_path
        image = cv2.imread(image_path)
        height, width = image.shape[0:2]

        with open(f"{save_path}{image_name}.txt", "a") as label_file:
            for bb in sample.bb_list:
                min_point, max_point = bb.get_bb_coordinates()
                xc_normal, yc_normal, h_normal, w_normal = convert_coordinates(min_point, max_point, height, width)

                print(f"{class_label} "
                      f"{xc_normal} "
                      f"{yc_normal} "
                      f"{w_normal} "
                      f"{h_normal}", file=label_file)


def check_one_sample(samples_dict, labels_path):
    random_sample = random.choice(list(samples_dict.values()))
    name = random_sample.image_path.split("/")[-1].split(".")[0]

    image = cv2.imread(random_sample.image_path)
    height, width = image.shape[:2]

    label_path = f"{labels_path}{name}.txt"
    with open(label_path, "r") as label_file:
        lines = label_file.readlines()

    for line in lines:
        points = line.strip().split(" ")[1:]
        x_center_norm, y_center_norm, box_width_norm, box_height_norm = map(float, points)

        x_center = int(x_center_norm * width)
        y_center = int(y_center_norm * height)
        box_width = int(box_width_norm * width)
        box_height = int(box_height_norm * height)

        x_min = int(x_center - box_width / 2)
        y_min = int(y_center - box_height / 2)
        x_max = int(x_center + box_width / 2)
        y_max = int(y_center + box_height / 2)

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow('test image to check', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





dataset_path = "../data/"
images_path = f"{dataset_path}images/"
labels_csv_path = f"{dataset_path}labels.csv"
labels_save_path = f"{dataset_path}labels/"

samples_dict = get_all_samples(labels_csv_path)
# convert2yolo_format(samples_dict, labels_save_path)
# check_one_sample(samples_dict, labels_save_path)