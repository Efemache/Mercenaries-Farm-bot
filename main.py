def main():
    log.info(f"Python version: {sys.version}")
    gen_images_new_resolution()

    while True:
        log.info("Loop")
        try:
            if win.find_game("Hearthstone"):
                where()
            elif win.find_game("Battle.net"):
                enter_from_battlenet()
        except KeyboardInterrupt as kerr:
            log.info("Keyboard Interrupt %s", kerr)
            sys.exit(0)
