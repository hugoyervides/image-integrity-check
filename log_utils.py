import csv

class LogUtils:
    def __init__(self, image_hashes):
        self.row_list = []
        self.row_list.append(
            ["Image_Hash"]
        )
        for (h, image_paths) in image_hashes.items():
            row = [h]
            row.extend(image_paths)
            self.row_list.append(row)


    def export(self, output_name):
        with open(output_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.row_list)
    