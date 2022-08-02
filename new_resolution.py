import os
import cv2

from modules.settings import settings_dict

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


def copy_dir_and_func_files(rootpath, srcdir, dstdir, ext, func, func_params):
    src = f"{rootpath}/{srcdir}"
    dst = f"{rootpath}/{dstdir}"
    os.path.exists(dst) or os.mkdir(dst)

    for name in os.listdir(src):
        if os.path.isdir(f"{src}/{name}"):
            print(f"Processing directory: {dst}/{name}... wait")
            copy_dir_and_func_files(
                rootpath, f"{srcdir}/{name}", f"{dstdir}/{name}", ext, func, func_params
            )
        else:
            extfile = f"{src}/{name}"
            if extfile.endswith(ext):
                func(extfile, f"{dst}/{name}", func_params)


new_resolution = settings_dict["monitor resolution"]

ox, oy = orig_resolution.split("x")
nx, ny = new_resolution.split("x")
if int(ox) / int(oy) == int(nx) / int(ny) and orig_resolution != new_resolution:
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
