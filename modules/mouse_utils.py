import random
import time

import pyautogui

from .settings import settings_dict


def mouse_click(btn="left"):
    pyautogui.click(button=btn)


def mouse_scroll(s):
    pyautogui.scroll(s)


def mouse_position(window):
    x, y = pyautogui.position()
    return (x - window[0], y - window[1])


def move_mouse_and_click(window, x, y):
    move_mouse(window, x, y, with_random=True)
    time.sleep(0.1)
    pyautogui.click()


def move_mouse(window, x, y, with_random=False):
    p = random.randint(-2, 2) if with_random else 0
    s = random.randint(-2, 2) if with_random else 0

    pyautogui.moveTo(
        window[0] + x + p,
        window[1] + y + s,
        settings_dict["mousespeed"],
        mouse_random_movement(),
    )


def mouse_random_movement():
    """define function to use several mouse movements on Windows & Linux"""
    return random.choices(
        [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad]
    )[0]
