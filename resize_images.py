import os
import cv2

from modules.settings import settings_dict

BASEDIR = "files"
orig_resolution = "1920x1080"

def browse_dir_and_resize_images(srcdir, dstdir, resolo="", resold=""):
    src = f"{BASEDIR}/{srcdir}"
    dst = f"{BASEDIR}/{dstdir}"
    os.path.exists(dst) or os.mkdir(dst)

    for name in os.listdir(src):
        if os.path.isdir(f"{src}/{name}"):
            print(f"Processing directory: {dst}/{name}... wait")
            browse_dir_and_resize_images(
                f"{srcdir}/{name}",
                f"{dstdir}/{name}",
                srcdir if resolo == "" else resolo,
                dstdir if resold == "" else resold,
            )
        else:
            imgfile = f"{src}/{name}"
            if imgfile.endswith(".png"):
                img = cv2.imread(imgfile, cv2.IMREAD_UNCHANGED)
                scale_percent = int(resold.split("x")[0]) / int(resolo.split("x")[0])
                width = int(img.shape[1] * scale_percent)
                height = int(img.shape[0] * scale_percent)

                # print(f"resize: {imgfile} -> {dst}/{name}")
                imgresized = cv2.resize(
                    img, (width, height), interpolation=cv2.INTER_CUBIC
                )
                cv2.imwrite(f"{dst}/{name}", imgresized)


new_resolution = settings_dict['monitor resolution']

ox, oy = orig_resolution.split("x")
nx, ny = new_resolution.split("x")
if int(ox) / int(oy) == int(nx) / int(ny) and orig_resolution != new_resolution:
    browse_dir_and_resize_images(orig_resolution, new_resolution)
else:
    print("Resolution not changed (1920x1080) or doesn't have the same ratio as 1920x1080")
