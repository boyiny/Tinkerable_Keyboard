from develop.controller_main import Controller_main

def main() -> None:
    if __name__ == 'develop.__main__':
        keyboard = Controller_main()
        keyboard.main()

if __name__ == "__main__":
    main()