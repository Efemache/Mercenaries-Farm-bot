import sys
import os.path

import cv2
import numpy as np


from .platforms import windowMP
from .mouse_utils import move_mouse_and_click, move_mouse

from .settings import settings_dict, jthreshold
from .constants import Action

import logging

# needed as workaround for Linux
# https://stackoverflow.com/questions/74856512/screenshot-error-xdefaultrootwindow-failed-after-closing-a-tkinter-toplevel
# https://github.com/BoboTiG/python-mss/issues/220
import mss

sct = mss.mss()
# workaround end ###

log = logging.getLogger(__name__)


def get_resolution() -> tuple[str, int, int, float]:
    """
    Get the resolution of the screen
    return tuple(resolution, width, height, scale_size)
    """
    try:
        resolution = settings_dict["resolution"]
        setting_size = resolution.split("x")
        setting_w, setting_h = int(setting_size[0]), int(setting_size[1])
        windows_w, windows_h = windowMP()[2], windowMP()[3]
        if round(windows_w / setting_w, 2) != round(windows_h / setting_h, 2):
            raise Exception(
                "setting resolution and windows resolution are not the same aspect ratio"
            )
        scale_size = setting_w / windows_w
        return resolution, setting_w, setting_h, scale_size
    except Exception as e:
        log.error(f"the resolution {resolution} is not supported: {e}")
        sys.exit(1)


def resize(img, width, height):
    """resize an image"""
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)


def get_gray_image(file):
    """load an OpenCV version of an image in memory and/or return it"""
    if not hasattr(get_gray_image, "imagesInMemory"):
        get_gray_image.imagesInMemory = {}

    # To Do : to resize the image so we can support other resolutions
    # screenshots was made on a 1920x1080 screen resolution
    # but with Hearthstone in windowed mode so it's like : 1920x1040
    # need to resize the image in memory
    if file not in get_gray_image.imagesInMemory:
        if not os.path.isfile(file):
            log.error(f'Err: file "{file}" doesn\'t exist.')
        get_gray_image.imagesInMemory[file] = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

        log.debug(f"images in memory : {len(get_gray_image.imagesInMemory)}")

    return get_gray_image.imagesInMemory[file]


def find_ellement(
    file, action, threshold="-", new_screen=True, speed=settings_dict["bot_speed"]
):
    """Find an object ('file') on the screen (UI, Button, ...)
        and do some actions ('action')
                Screenshot Here  |    Screenshot Before  |  Actions   | Return
    action = 1 :       x         |                       |     -      | True / False
    action = 2 :       x         |                       |    move    | True / False
    action = 14:       x         |                       | move+click | True / False
    action = 12:                 |           x           |     -      |  x,y / 0,0
    action = 15:       x         |                       |     -      |  x,y / 0,0
      (new action needed to return a tab of object/coordinates)
    """
    click_coords = find_element_from_file(
        file,
        new_screenshot=new_screen,
        threshold=threshold,
        speed=speed,
    )
    if click_coords is not None:
        x, y = click_coords
        if action in [
            Action.get_coords_part_screen,
            Action.get_coords,
            Action.screenshot,
        ]:
            return click_coords
        elif action == Action.move:
            window = windowMP()
            move_mouse(window, x, y)
            return True
        elif action == Action.move_and_click:
            # move mouse and click
            window = windowMP()
            move_mouse_and_click(window, x, y)
            return True
    elif action in [Action.get_coords_part_screen, Action.get_coords]:
        return None
    return False


def find_element_from_file(
    file,
    new_screenshot=True,
    threshold="-",
    speed=settings_dict["bot_speed"],
):
    """Find Element Center from template filename

    Args:
        file (str): filename of template
        new_screenshot (bool, optional): Whether to take a new screenshot image or not.
            Defaults to True.
        threshold (str, optional): Threshold of whether a comparison is good enough.
            Defaults to "-".
        speed (int, optional): Time in seconds to sleep before comparison.
            Defaults to settings_dict["bot_speed"].

    Returns:
        (int, int): coordinates of center of element
    """

    if threshold == "-":
        if file in jthreshold and jthreshold[file] != "-":
            threshold = jthreshold[file]
        else:
            threshold = jthreshold["default_grey"]

    resolution, width, height, scale_size = get_resolution()

    # choose if the bot need to look into the window or in a part of the window
    if new_screenshot is True:
        top = 0
        left = 0
        find_element_from_file.partImg = partscreen(
            windowMP()[2],
            windowMP()[3],
            windowMP()[1],
            windowMP()[0],
            resize_width=width,
            resize_height=height,
        )
    else:
        top = new_screenshot[2] - windowMP()[1]
        left = new_screenshot[3] - windowMP()[0]
        find_element_from_file.partImg = partscreen(
            new_screenshot[0],
            new_screenshot[1],
            new_screenshot[2],
            new_screenshot[3],
            scale_size=scale_size,
        )

    img = cv2.cvtColor(find_element_from_file.partImg, cv2.COLOR_BGR2GRAY)

    template = get_gray_image(f"files/{resolution}/{file}")

    click_coords = find_element_center_on_screen(img, template, threshold, scale_size)

    if click_coords is not None:
        click_coords = [click_coords[0] + left, click_coords[1] + top]
        log.info(
            f"Found {file} ( {threshold} ) { click_coords[0] } { click_coords[1] }",
        )
    else:
        log.info(f"Looked for {file} ( {threshold} )")

    return click_coords


def partscreen(
    x,
    y,
    top,
    left,
    debug_mode=False,
    resolution=None,
    resize_width=None,
    resize_height=None,
    scale_size=1,
):
    """
    take screeenshot for a part of the screen to find some part of the image
    """

    # workaround for Linux  (read more info at the top of this file)
    # with mss.mss() as sct:
    global sct
    monitor = {"top": top, "left": left, "width": x, "height": y}
    sct_img = sct.grab(monitor)

    if debug_mode:
        output_file = "files/debug.png"
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)

    partImg = np.array(sct_img)

    if resize_width and resize_height:
        partImg = cv2.resize(
            partImg, (resize_width, resize_height), interpolation=cv2.INTER_CUBIC
        )
    elif scale_size != 1:
        partImg = cv2.resize(
            partImg,
            (int(x * scale_size), int(y * scale_size)),
            interpolation=cv2.INTER_CUBIC,
        )

    return partImg


def find_element_center_on_screen(img, template, threshold=0, scale_size=1):
    """Finds Element if on screen and returns center

    Args:
        img (numpy.ndarray): full image of window
        template (numpy.ndarray): smaller image we are looking for
        threshold (int, optional): threshold to determine if match meets our standards.
            Defaults to 0.

    Returns:
        center_coords: center coordinates of the best match found
    """
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    h = template.shape[0] // 2
    w = template.shape[1] // 2
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    return (
        ((max_loc[0] + w) / scale_size, (max_loc[1] + h) / scale_size)
        if max_val > threshold
        else None
    )
