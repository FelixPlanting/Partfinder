from emails import get_messages
from gui import launch_ui


def main():
    launch_ui(get_messages)


if __name__ == "__main__":
    main()
