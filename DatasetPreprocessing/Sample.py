class BoundingBox:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def get_bb_coordinates(self):
        return (self.x_min, self.y_min), (self.x_max, self.y_max)

class Sample:
    def __init__(self, image_filepath: str):
        self.image_path = image_filepath
        self.bb_list = []

    def add_bb(self, x_min: float, y_min: float, x_max: float, y_max: float):
        self.bb_list.append(BoundingBox(x_min, y_min, x_max, y_max))