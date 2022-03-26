import time

import cv2
import numpy as np


from .platform import windowMP
from .mouse_utils import move_mouse_and_click, move_mouse
from .debug import debug
from .settings import settings_dict, jthreshold
from .constants import Action

# This is a guess since the window.rect function returns (-8, -8, 1936, 1056) for me
default_rect = (-8, -8, 1936, 1056)

default_width = default_rect[2] - default_rect[0]
default_height = default_rect[3] - default_rect[1]
#imagesInMemory={}

def get_gray_image(file, width=1920, height=1040) :
    """ load an OpenCV version of an image in memory and/or return it
    """
    if not hasattr(get_gray_image, "imagesInMemory"):
        get_gray_image.imagesInMemory = {}

    # To Do : to resize the image so we can support other resolutions
    # screenshots was made on a 1920x1080 screen resolution but with Hearthstone in windowed mode so it's like : 1920x1040
    # need to resize the image in memory
    if not file in get_gray_image.imagesInMemory :
        get_gray_image.imagesInMemory[file] = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    debug("images in memory : ", len(get_gray_image.imagesInMemory))
    return get_gray_image.imagesInMemory[file]


def find_ellement(file, action, threshold="-", speed=settings_dict["bot_speed"]):
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
    debug("DEBUG : find_ellement_grey START")

    click_coords = find_element_from_file(
        file,
        new_screenshot=action != Action.get_coords_part_screen,
        threshold=threshold,
        speed=speed,
    )
    if click_coords is not None:
        x, y = click_coords
        if action in [Action.get_coords_part_screen, Action.get_coords]:
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
    file, new_screenshot=True, threshold="-", speed=settings_dict["bot_speed"]
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
    debug("DEBUG : find_element_grey START")
    global partImg
    time.sleep(speed)

    if threshold == "-":
        if file in jthreshold and jthreshold[file] != "-":
            threshold = jthreshold[file]
        else:
            threshold = jthreshold["default_grey"]

    # choose if the bot need to look into the screen or in a part of the screen
    if new_screenshot:
        partscreen(windowMP()[2], windowMP()[3], windowMP()[1], windowMP()[0])

    img = cv2.cvtColor(partImg, cv2.COLOR_BGR2GRAY)
    monitor_resolution = settings_dict["monitor resolution"]
    template = get_gray_image(f"files/{monitor_resolution}/{file}")

    click_coords = find_element_center_on_screen(img, template, threshold=threshold)

    if click_coords is not None:
        print(f"Found {file}", "(", threshold, ")", *click_coords)
    else:
        print(f"Looked for {file}", "(", threshold, ")")

    return find_element_center_on_screen(img, template, threshold=threshold)


def partscreen(x, y, top, left, debug_mode=False, monitor_resolution=None):
    """
    take screeenshot for a part of the screen to find some part of the image
    """
    global partImg
    debug("entered screenpart")
    import mss.tools

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        sct_img = sct.grab(monitor)

        if debug_mode:
            output_file = f"files/{ monitor_resolution}/part.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)
        partImg = np.array(sct_img)
    return partImg


#def get_gray_image(file, width=default_width, height=default_height):
#    """load an OpenCV version of an image in memory and/or return it"""
#    # To Do : to resize the image so we can support other resolutions
#    # screenshots was made on a 1920x1080 screen resolution
#    # but with Hearthstone in windowed mode so it's like : 1920x1040
#    # need to resize the image in memory
#    if file not in imagesInMemory:
#        imagesInMemory[file] = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
#
#    return imagesInMemory[file]


def find_element_center_on_screen(img, template, threshold=0):
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

    return (max_loc[0] + w, max_loc[1] + h) if max_val > threshold else None
