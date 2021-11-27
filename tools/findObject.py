import cv2
import numpy as np
from mss import mss
import mss
import sys

""" If the bot doesn't find an object (Button, UI Element, ...), use this script
to test it and find the right 'threshold'
"""

if len(sys.argv) == 4 : 
    print("arg: 3")
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    imgTmpPath = sys.argv[2]
    threshold = float(sys.argv[3])
elif  len(sys.argv) == 3 : 
    print("arg: 2")
    sct = mss.mss()
    img = np.array(sct.grab(sct.monitors[1]))
    imgTmpPath = sys.argv[1]
    threshold = float(sys.argv[2])
else : 
    print("Usage : ")
    print("")
    print(sys.argv[0],"'/path/to/screenshot.png' '/path/to/the/imageObject/to/find.png' <threshold>")
    print("     will try to find your object in your screenshot")
    print("")
    print(sys.argv[0],"'/path/to/the/imageObject/to/find.png' <threshold>")
    print("     will take a screenshot to compare with your object")
    print("")
    print("THRESHOLD : float from 0 to 1 (try with something between 0.75 (less precise)  and 0.95 (more precise) and add/rm 0.5 to 0.1)")
    print("")
    print("Example: ")
    print("         ",sys.argv[0],"/home/user/myscreenshot.png /home/user/theButtonToFind.png 0.81")
    print("")
    exit(1)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread(imgTmpPath, cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)


loc = np.where(result >= threshold)
if len(loc[0]) != 0 :
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        break
    print("Found ", pt[0], pt[1] )
    print("Use 'Echap' on your keyboard to exit.")
    cv2.imshow("Keyboard: 'Echap' to exit", img)
    while True:
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()
else :
    print("Not found " )

