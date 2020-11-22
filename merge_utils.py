import os
import shutil

class MergeUtils:
    def __init__(self, image_hashes):
        self.image_hashes = image_hashes
        self.prefix = "IMG_"
    
    def merge(self, destination_folder):
        #Create the destination folder
        try:
            os.mkdir(destination_folder)
        except:
            pass
        counter = 0
        for (h, image_paths) in self.image_hashes.items():
            #Check if we have an image
            if len(image_paths) > 0:
                ext = os.path.splitext(image_paths[0])[-1]
                target = os.path.join(destination_folder, self.prefix + str(counter) + ext)
                shutil.move(image_paths[0], target)
                #Delete the duplicated images
                for i in range(1, len(image_paths)):
                    os.remove(image_paths[i])
                counter += 1
            else:
                print("[ERROR] hash " + str(h) + " does not contain a valid path!")


