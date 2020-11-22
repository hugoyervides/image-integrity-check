import cv2
from imutils import paths

def hash_image(image, hashSize = 8):
    #Convert image to grayscale and resize the image
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.resize(gray_img, (hashSize + 1, hashSize))

    #Compute the horizontal gradient between adjacent column pixels
    diff = resized_img[:, 1:] > resized_img[:, :-1]

    # convert the difference image to a hash and return it
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def get_image_paths(path):
    return list(paths.list_images(path))

def compute_images(image_paths, return_hashes):
    for image_path in image_paths:
        #Load the image
        image = cv2.imread(image_path)
        image_hash = hash_image(image)

        #Load all the images with that hash and add the current image and update the map
        images = return_hashes.get(image_hash, [])
        images.append(image_path)
        return_hashes[image_hash] = images

def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out