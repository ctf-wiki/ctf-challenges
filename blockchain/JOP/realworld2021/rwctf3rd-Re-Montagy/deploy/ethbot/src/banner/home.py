#!/usr/bin/python3
import sys
from src.banner.text.corpus import MENU, WELCOME, SRC_TEXT
from src.banner.Sections import Creation, Deploy, Checker, Source
from src.utils.prettyprint.Red import Formator


def selection(ctx, choice):
    if choice == '1':
        Creation.run(ctx)
    elif choice == '2':
        Deploy.run(ctx)
    elif choice == '3':
        Checker.run(ctx)
    else:
        print("Invalid option")
        sys.exit(0)



def menu(ctx):
    f = Formator()
    #f.screen.clear_screen()
    #print(f.in_all_left(""))
    print(WELCOME)
    print(MENU)

    # get choice
    choice = input("[-]input your choice: ")

    selection(ctx, choice)

