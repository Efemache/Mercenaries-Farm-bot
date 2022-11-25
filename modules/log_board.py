import time
import os
import re
from pathlib import Path
import threading
import logging

log = logging.getLogger(__name__)


class LogHSMercs:
    def __init__(self, logpath):
        """generator function that yields new lines in filelog to
        follow cards in hand and on the battlefield
        """
        self.logpath = logpath

        Path(logpath).touch(exist_ok=True)
        self.cardsInHand = []
        self.myBoard = {}
        self.mercsId = {}

        self.enemiesBoard = {}
        self.enemiesId = {}

        self.zonechange_finished = False

    def follow(self):
        # go to the end of the file
        self.logfile.seek(0, os.SEEK_END)

        regexBoard = (
            ".+? tag=ZONE_POSITION "
            ".+?entityName=(.+?) +"
            "id=(.+?) "
            ".+?zonePos=(.) "
            "cardId=.+? "
            "player=1\] .+? "
            "dstPos=(.)"
        )
        regexEnemyBoard = (
            ".+?entityName=(.+?) +"
            "id=(.+?) "
            ".+?zonePos=(.) "
            "cardId=.+? "
            "player=2\] .+? "
            "dstZoneTag=PLAY "
            "dstPos=(.)"
        )
        regexEnemyBoardUpdate = (
            ".+? tag=ZONE_POSITION "
            ".+?entityName=(.+?) +"
            "id=(.+?) "
            ".+?zonePos=(.) "
            "cardId=.+? "
            "player=2\] .+? "
            "dstPos=(.)"
        )
        regexInHand = (
            ".+?entityName=(.+?) +"
            "id=.+ "
            ".+?cardId=.+? player=3\] .+? "
            "dstZoneTag=HAND .+?"
        )
        # D 14:25:59.2307890 ZoneChangeList.ProcessChanges() - processing index=4 change=powerTask=[power=[type=TAG_CHANGE entity=[id=5 cardId=LETL_006H_01 name=Lord Jaraxxus] tag=FAKE_ZONE value=3 ] complete=False] entity=[entityName=Lord Jaraxxus id=5 zone=SETASIDE zonePos=0 cardId=LETL_006H_01 player=3] srcZoneTag=INVALID srcPos= dstZoneTag=HAND dstPos=

        regexGoToEnemy = (
            ".+?entityName=.+? +"
            "id=.+? zone=PLAY "
            "zonePos=(.) "
            ".+?zone from FRIENDLY PLAY -> OPPOSING PLAY"
        )
        # ZoneChangeList.ProcessChanges() - id=28 local=False [entityName=Spud M.E. 1 id=62 zone=PLAY zonePos=1 cardId=LETL_903t_01 player=2] zone from FRIENDLY PLAY -> OPPOSING PLAY

        # start infinite loop to read log file
        while self.__running:
            # read last line of file
            line = self.logfile.readline()
            # sleep if file hasn't been updated
            if not line:
                time.sleep(0.1)
                continue

            if "ZoneChangeList.ProcessChanges() - processing" in line and re.search(
                regexBoard, line
            ):
                (mercenary, mercId, srcpos, dstpos) = re.findall(regexBoard, line)[0]
                self.mercsId[mercId] = mercenary
                # srcpos = actual position.
                # =0 if it hasn't any previous position
                if (
                    srcpos != "0"
                    and srcpos in self.myBoard
                    and self.myBoard[srcpos] == mercId
                ):
                    self.myBoard.pop(srcpos)

                # dstpos = 0 if the card is going to GRAVEYARD
                if dstpos != "0":
                    self.myBoard[dstpos] = mercId

            elif "ZoneChangeList.ProcessChanges() - processing" in line and re.search(
                regexEnemyBoard, line
            ):
                (enemy, enemyId, srcpos, dstpos) = re.findall(regexEnemyBoard, line)[0]
                self.enemiesId[enemyId] = enemy
                # srcpos = actual position.
                # =0 if it hasn't any previous position
                if (
                    srcpos != "0"
                    and srcpos in self.enemiesBoard
                    and self.enemiesBoard[srcpos] == enemyId
                ):
                    self.enemiesBoard.pop(srcpos)

                # dstpos = 0 if the card is going to GRAVEYARD
                if dstpos != "0":
                    self.enemiesBoard[dstpos] = enemyId

            elif "ZoneChangeList.ProcessChanges() - processing" in line and re.search(
                regexEnemyBoardUpdate, line
            ):
                (enemy, enemyId, srcpos, dstpos) = re.findall(
                    regexEnemyBoardUpdate, line
                )[0]
                self.enemiesId[enemyId] = enemy
                # srcpos = actual position.
                # =0 if it hasn't any previous position
                if (
                    srcpos != "0"
                    and srcpos in self.enemiesBoard
                    and self.enemiesBoard[srcpos] == enemyId
                ):
                    self.enemiesBoard.pop(srcpos)

                # dstpos = 0 if the card is going to GRAVEYARD
                if dstpos != "0":
                    self.enemiesBoard[dstpos] = enemyId
            elif "ZoneChangeList.ProcessChanges() - processing" in line and re.search(
                regexInHand, line
            ):
                mercenary = re.findall(regexInHand, line)[0]
                if mercenary not in self.cardsInHand:
                    self.cardsInHand.append(mercenary)

            elif " ZoneChangeList.ProcessChanges() " in line and re.search(
                regexGoToEnemy, line
            ):
                zonepos = re.findall(regexGoToEnemy, line)[0]
                self.myBoard.pop(zonepos)

            elif "ZoneMgr.AutoCorrectZonesAfterServerChange()" in line:
                self.zonechange_finished = True

    def get_zonechanged(self):
        if self.zonechange_finished:
            self.zonechange_finished = False
            return True
        else:
            return False

    def start(self):
        log.debug("Reading logfile: %s", self.logpath)
        self.logfile = open(self.logpath, "r", encoding="UTF-8")
        self.__running = True
        t1 = threading.Thread(target=self.follow)
        self.thread = t1
        t1.start()

    def stop(self):
        # self.thread.stop()
        log.debug("Closing logfile: %s", self.logpath)
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
        self.enemiesBoard = {}
        self.enemiesId = {}

    def getMyBoard(self):
        return {key: self.mercsId[self.myBoard[key]] for key in self.myBoard.keys()}

    def getEnemyBoard(self):
        return {
            key: self.enemiesId[self.enemiesBoard[key]]
            for key in self.enemiesBoard.keys()
        }
