from abc import ABC, abstractmethod


class WindowMgr(ABC):
    @abstractmethod
    def get_window_geometry(self):
        pass

    @abstractmethod
    def find_game(self):
        pass
