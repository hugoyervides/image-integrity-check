import numpy as np
import cv2
import os
from image_utils import hash_image, get_image_paths, compute_images, chunk_it
import multiprocessing
from argument_parser import ArgumentParser
from log_utils import LogUtils
from merge_utils import MergeUtils

if __name__ == "__main__":
    #Init argument parser
    a_parser = ArgumentParser([
        {
            "short_name": '-f1',
            "long_name": "--folder1",
            "required": True,
            "help": "Path to first folder"
        },
        {
            "short_name": '-f2',
            "long_name": "--folder2",
            "required": True,
            "help": "Path to second folder"
        },
        {
            "short_name": '-l',
            "long_name": "--log",
            "required": False,
            "help": "Export log as CSV"
        },
        {
            "short_name": '-m',
            "long_name": '--merge',
            "required": False,
            "help": "Merge both folders in one"
        }
    ])
    args = a_parser.get_args()

    image_paths = []
    image_paths.append(get_image_paths(args['folder1']))
    print("[INFO] Found " + str(len(image_paths[-1])) + " images in first folder!")
    image_paths.append(get_image_paths(args["folder2"]))
    print("[INFO] Found " + str(len(image_paths[-1])) + " images in second folder!")

    #Find number of cores
    n_cores = multiprocessing.cpu_count()
    print("[INFO] Number of CPUs: " + str(n_cores))

    manager = multiprocessing.Manager()
    return_hashes = manager.dict()
    jobs = []

    #Compute folders
    for i, paths in enumerate(image_paths):
        print("[INFO] Computing folder " + str(i))
        #Divide the image set into chunks for each core
        image_chunks = chunk_it(paths, n_cores)

        for i, chunk in enumerate(image_chunks):
            p = multiprocessing.Process(target = compute_images, args=(chunk, return_hashes))
            print("[INFO] Processing " + str(len(chunk)) + " images in CPU No. " + str(i))
            jobs.append(p)
            p.start()    

        for proc in jobs:
            proc.join()

    #Check if we need to export logs
    if "log" in args:
        LogUtils(return_hashes).export(args['log'])

    if "merge" in args:
        MergeUtils([args["folder1"], args["folder2"]], return_hashes).merge(args['merge'])

    #Check for missing images
    for (h, image_paths) in return_hashes.items():
        if len(image_paths) <= 1:
            print("[WARNING] Image integrity check failed! for " + image_paths[0])
