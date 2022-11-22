import os
import time as t
from styles import Styles as s
import ast

padding = "=" * 25


def admin_banner(num):
    if num == 1:
        os.system("cls")
        print(s.pr_bold((f"{padding} ~ MENU ~ {padding}\n")))
        print(
            f"\t\tYou have selected: {s.pr_bold('Word Settings')}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f"\t\t\t{s.pr_bold('1')}: Add word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('2')}: Remove word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('3')}: Edit word")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('4')}: View wordlist")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('5')}: {s.pr_red('*** Reset Words ***')}")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('6')}: Toggle Words")
        t.sleep(0.05)
        print(f"\t\t\t{s.pr_bold('7')}: Back")
    elif num == 2:

        print(
            s.pr_green(
                (
                    r""" █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗    ██████╗  █████╗ ███╗   ██╗███████╗██╗     
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║    ██████╔╝███████║██╔██╗ ██║█████╗  ██║     
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║    ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║    ██║     ██║  ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                                      """
                )
            )
        )
    elif num == 3:
        try:
            with open("../data/game_settings.txt", "r") as f:
                obj = ast.literal_eval(f.read())
        except FileNotFoundError:
            print("Error. Settings not found. ")
        os.system("cls")
        print(s.pr_bold((f"\n\n\n{padding} ~ MENU ~ {padding}\n")))
        print(f"\tYou have selected: {s.pr_bold('Game Settings')}\n")
        t.sleep(0.05)
        print(f"\t\tNumber of sessions: {s.pr_bold(obj['number of attempts'])}")
        t.sleep(0.05)
        print(
            f"\t\tNumber of guesses per session: {s.pr_bold(obj['number of guesses'])}"
        )
        t.sleep(0.05)
        print(
            f"\t\tNumber of top players on leaderboard: {s.pr_bold(obj['number of top players'])}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f" {s.pr_bold('1')}: Edit number of sessions")
        t.sleep(0.05)
        print(f" {s.pr_bold('2')}: Edit number of attempts/guesses")
        t.sleep(0.05)
        print(f" {s.pr_bold('3')}: Edit number of top players")
        t.sleep(0.05)
        print(f" {s.pr_bold('4')}: Back\n")
    elif num == 4:
        os.system("cls")
        print(s.pr_bold((f"{padding} ~ MENU ~ {padding}\n")))
        print(
            f"\tYou have selected: {s.pr_bold('View Reports')}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f"\t\t{s.pr_bold('1')}: Print Leaderboard")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('2')}: Filter Log")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('3')}: Remove Log")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('4')}: Back")
    elif num == 5:
        os.system("cls")
        print(s.pr_bold((f"{padding} ~ MENU ~ {padding}\n")))
        print(
            f"\tYou have selected: {s.pr_bold('Admin Settings')}\n\n{s.pr_bold(padding * 2 + '==========')}\n"
        )
        print(f"\t\t{s.pr_bold('1')}: Create Admin")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('2')}: Delete Admin")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('3')}: View Admins")
        t.sleep(0.05)
        print(f"\t\t{s.pr_bold('4')}: Back")
    elif num == 6:
        print(
            s.pr_bold(
                """██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
                                       """
            )
        )
