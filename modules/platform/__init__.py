from .factory import get_window_manager as _get_window_manager


win = _get_window_manager()
windowMP = win.get_window_geometry


__all__ = ["windowMP", "win"]
