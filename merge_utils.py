import os

class MergeUtils:
    def __init__(self, folders, image_hashes):
        self.folders = folders
        self.image_hashes = image_hashes
    
    def merge(destination_folder):
        os.mkdir(destination_folder)
        os.chdir(destination_folder)
        for (h, image_paths) in self.image_hashes.items():
            for folder in self.folders:
                if image_paths[0].find(folder) != -1:
                    