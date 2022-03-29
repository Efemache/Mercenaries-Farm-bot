class MercenariesFarmBaseException(Exception):
    pass


class SettingsError(MercenariesFarmBaseException):
    pass


class MissingGameDirectory(SettingsError):
    pass


class UnsetGameDirectory(SettingsError):
    pass


class WindowManagerError(MercenariesFarmBaseException):
    pass


class AHKNotInstalled(WindowManagerError):
    pass


class NoWindowManagerFound(WindowManagerError):
    pass
