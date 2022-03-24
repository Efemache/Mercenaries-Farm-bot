import time
import os
import re
from pathlib import Path
import threading


class LogHSMercs:
    def follow(self):
        # go to the end of the file
        self.logfile.seek(0, os.SEEK_END)

        regexBoard = (
            ".+? tag=ZONE_POSITION "
            ".+?entityName=(.+?) "
            "id=(.+?) "
            ".+?zonePos=(.) "
            "cardId=.+? "
            "player=1\] .+? "
            "dstPos=(.)"
        )

        # start infinite loop to read log file
        while self.__running:
            # read last line of file
            line = self.logfile.readline()
            # sleep if file hasn't been updated
            if not line:
                time.sleep(0.1)
                continue
            if "ZoneChangeList.ProcessChanges() - processing" in line:
                if re.search(regexBoard, line):

                    (mercenary, mercId, srcpos, dstpos) = re.findall(regexBoard, line)[
                        0
                    ]
                    self.mercsId[mercId] = mercenary
                    # srcpos = actual position.
                    # =0 if it hasn't any previous position
                    if srcpos != "0":
                        if srcpos in self.myBoard and self.myBoard[srcpos] == mercId:
                            self.myBoard.pop(srcpos)

                    # dstpos = 0 if the card is going to GRAVEYARD
                    if dstpos != "0":
                        self.myBoard[dstpos] = mercId

    def start(self):
        self.logfile = open(self.logpath, "r")
        self.__running = True
        t1 = threading.Thread(target=self.follow)
        self.thread = t1
        t1.start()

    def stop(self):
        # self.thread.stop()
        self.__running = False
        self.cleanHand()
        self.cleanBoard()
        self.logfile.close()

    def cleanHand(self):
        self.cardsInHand = []

    def getHand(self):
        return self.cardsInHand

    def cleanBoard(self):
        self.myBoard = {}
        self.mercsId = {}

    def getBoard(self):
        board = {}
        for key in self.myBoard.keys():
            board[key] = self.mercsId[self.myBoard[key]]
        return board

    def __init__(self, logpath):
        """generator function that yields new lines in filelog to
        follow cards in hand and on the battlefield
        """
        self.logpath = logpath

        Path(logpath).touch(exist_ok=True)
        self.cardsInHand = []
        self.myBoard = {}
        self.mercsId = {}
