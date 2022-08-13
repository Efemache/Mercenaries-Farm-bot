import cv2

from modules.settings import settings_dict
from modules.file_utils import copy_dir_and_func_files

BASEDIR = "files"
orig_resolution = "1920x1080"


def resize_image(srcfile, dstfile, params=[]):
    resolo = params[0]
    resold = params[1]

    img = cv2.imread(srcfile, cv2.IMREAD_UNCHANGED)
    scale_percent = int(resold.split("x")[0]) / int(resolo.split("x")[0])
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)

    # print(f"resize: {imgfile} -> {dst}/{name}")
    imgresized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dstfile, imgresized)


new_resolution = settings_dict["resolution"]

ox, oy = orig_resolution.split("x")
nx, ny = new_resolution.split("x")

if round(int(ox) / int(oy), 2) == round(int(nx) / int(ny), 2) and orig_resolution != new_resolution:
    copy_dir_and_func_files(
        BASEDIR,
        orig_resolution,
        new_resolution,
        ".png",
        resize_image,
        [orig_resolution, new_resolution],
    )
else:
    print(
        "Resolution not changed (1920x1080) or doesn't have the same ratio as 1920x1080"
    )
