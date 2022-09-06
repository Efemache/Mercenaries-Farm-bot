import cv2

from .settings import settings_dict
from .file_utils import copy_dir_and_func_files

import logging

log = logging.getLogger(__name__)

BASEDIR = settings_dict["root_images_dir"]
orig_resolution = settings_dict["default_resolution"]


def resize_image(srcfile, dstfile, params=[]):
    """resize image from source to destination"""
    orig_resolution_w = int(params[0].split("x")[0])
    new_resolution_w = int(params[1].split("x")[0])

    img = cv2.imread(srcfile, cv2.IMREAD_UNCHANGED)
    scale_ratio = new_resolution_w / orig_resolution_w
    width = int(img.shape[1] * scale_ratio)
    height = int(img.shape[0] * scale_ratio)

    # print(f"resize: {srcfile} -> {dstfile}")

    # INTER_AREA INTER_CUBIC INTER_LANCZOS4 INTER_LINEAR INTER_NEAREST
    imgresized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dstfile, imgresized)


def gen_images_new_resolution():
    new_resolution = settings_dict["resolution"]

    ox, oy = orig_resolution.split("x")
    nx, ny = new_resolution.split("x")

    if orig_resolution == new_resolution:
        log.debug(f"Resolution not changed : {orig_resolution}")
    else:
        # Resolution modified so we need to generate images
        # we check it's the same ratio as the original images
        if round(int(ox) / int(oy), 2) == round(int(nx) / int(ny), 2):
            copy_dir_and_func_files(
                f"{BASEDIR}/{orig_resolution}",
                f"{BASEDIR}/{new_resolution}",
                ".png",
                resize_image,
                [orig_resolution, new_resolution],
            )
        else:
            log.error(f"Resolution doesn't have the same ratio as {orig_resolution}")
