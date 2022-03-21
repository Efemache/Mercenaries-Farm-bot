debug_mode = False


def debug(*message):
    if debug_mode:
        print("[DEBUG] ", message)
