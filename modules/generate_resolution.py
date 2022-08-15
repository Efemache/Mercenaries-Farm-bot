import os
import shutil

import cv2

from .image_utils import get_resolution
from .settings import settings_dict
from .file_utils import copy_dir_and_func_files

FILES_DIR = "files"
TEMP_DIR = "tmp"
orig_resolution = "1920x1080"


def resize_image(srcfile, dstfile, params=[]):
    orig_resolution_w = int(params[0].split("x")[0])
    new_resolution_w = int(params[1].split("x")[0])

    img = cv2.imread(srcfile, cv2.IMREAD_UNCHANGED)
    scale_size = orig_resolution_w / new_resolution_w
    new_w = int(img.shape[1] * scale_size)
    new_h = int(img.shape[0] * scale_size)

    print(f"resize: {srcfile} ({img.shape[1]},{img.shape[0]}) -> {dstfile} ({new_w},{new_h})")
    imgresized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dstfile, imgresized)

def generate_temp_resolution():
    new_resolution, _, _, _ = get_resolution()

    # clear tmp folder
    os.path.exists(TEMP_DIR) and os.remove(TEMP_DIR)

    if orig_resolution == new_resolution:
        shutil.copytree(FILES_DIR, TEMP_DIR)
        return

    copy_dir_and_func_files(
        f"{FILES_DIR}/{orig_resolution}",
        f"{TEMP_DIR}/{new_resolution}",
        ".png",
        resize_image,
        [orig_resolution, new_resolution],
    )
