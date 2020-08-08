import os
import platform
from datetime import datetime

LOGO = """\033[31m ██████╗██╗      ██████╗ ██╗   ██╗██████╗ ██╗███████╗██╗   ██╗
██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗██║██╔════╝╚██╗ ██╔╝
██║     ██║     ██║   ██║██║   ██║██║  ██║██║█████╗   ╚████╔╝
██║     ██║     ██║   ██║██║   ██║██║  ██║██║██╔══╝    ╚██╔
╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝██║██║        ██║
 ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚═╝        ╚═╝\033[0m"""


class Console:
    def __init__(self):
        self.log_track = []
        self.log_file_name = "CLoudify.log"
        self.log_file = open(self.log_file_name, 'a')
        self.output()

    def clear_screen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def logo(self):
        print(LOGO)

    def output(self):
        self.clear_screen()
        self.logo()
        print()
        for item in self.log_track[-5:]:
            print(item)

    def log(self, log_item, negative=False):
        color_code = "\033[7;32m"
        if negative:
            color_code = "\033[7;31m"

        timestamp = datetime.now().strftime("%Y/%M/%D %H:%m")
        item = f"{color_code}[{timestamp}]\033[0m {log_item}"

        self.log_file.write(f"[{timestamp}] {log_item}\n")
        self.log_track.append(item)
        self.output()


if __name__ == "__main__":
    console = Console()
    console.log("CONSOLE STARTED")
    console.log("test", negative=True)
