import time

import cv2
import numpy as np


from .platform import windowMP
from .mouse_utils import move_mouse_and_click, move_mouse
from .debug import debug
from .settings import settings_dict, jthreshold
from .constants import Action


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
    #    global threshold
    global screenImg
    global partImg
    time.sleep(speed)
    retour = False

    if threshold == "-":
        if file in jthreshold and jthreshold[file] != "-":
            threshold = jthreshold[file]
        else:
            threshold = jthreshold["default_grey"]

    # choose if the bot need to look into the screen or in a part of the screen
    if action != Action.get_coords_part_screen:
        partscreen(windowMP()[2], windowMP()[3], windowMP()[1], windowMP()[0])

    img = cv2.cvtColor(partImg, cv2.COLOR_BGR2GRAY)
    monitor_resolution = settings_dict["Monitor Resolution"]
    template = cv2.imread(f"files/{monitor_resolution}/{file}", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    h = template.shape[0]
    w = template.shape[1]

    loc = np.where(result >= threshold)
    if len(loc[0]) != 0:
        retour = True
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x = int((pt[0] * 2 + w) / 2)
        y = int((pt[1] * 2 + h) / 2)
        print(f"Found {file}", "(", threshold, ")", x, y)
        if action in [Action.get_coords_part_screen, Action.get_coords]:
            retour = (x, y)
        elif action == Action.move:
            window = windowMP()
            move_mouse(window, x, y)
        elif action == Action.move_and_click:
            # move mouse and click
            window = windowMP()
            move_mouse_and_click(window, x, y)

    else:
        print(f"Looked for {file}", "(", threshold, ")")
        if action in [Action.get_coords_part_screen, Action.get_coords]:
            retour = (0, 0)
    return retour


def partscreen(x, y, top, left, debug_mode=False, monitor_resolution=None):
    """
    take screeenshot for a part of the screen to find some part of the image
    """
    global partImg
    debug("entered screenpart")
    import mss.tools

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        # output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        # mss.tools.to_png(
        #   sct_img.rgb,
        #   sct_img.size,
        #   output='files/' + settings_dict['Monitor Resolution'] + '/part.png'
        # )
        if debug_mode:
            output_file = f"files/{ monitor_resolution}/part.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)
        partImg = np.array(sct_img)
    return partImg
