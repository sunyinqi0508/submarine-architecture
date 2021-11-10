import sys

from argparse import ArgumentParser
from multiprocessing import Process
from time import sleep

from submarine_server import GameServer

from clients.submarine_captain_client import SubmarineCaptain
from clients.trench_manager_client import TrenchManager

from clients.manual_clients.submarine_captain_client import ManualSubmarineCaptain
from clients.manual_clients.trench_manager_client import ManualTrenchManager

def init_submarine_captain(name, is_manual_mode, fd):
    sleep(1)
    player = SubmarineCaptain(name=name) if not is_manual_mode else ManualSubmarineCaptain(name=name, fd=fd)
    player.play_game()

def init_trench_manager(name, is_manual_mode, fd):
    sleep(1)
    player = TrenchManager(name=name) if not is_manual_mode else ManualTrenchManager(name=name, fd=fd)
    player.play_game()

def main():
    parser = ArgumentParser()
    parser.add_argument("--manual", help="Allows you to choose which player you'd like to play manually: 'sub', 'trench', or 'both'")
    args = parser.parse_args()

    is_submarine_manual = is_trench_manual = False
    if args.manual == 'both':
        is_submarine_manual = is_trench_manual = True
    elif args.manual == 'sub':
        is_submarine_manual = True
    elif args.manual == 'trench':
        is_trench_manual = True

    player_1 = Process(target=init_submarine_captain, args=('Captain Joe', is_submarine_manual, sys.stdin.fileno()))
    player_1.start()
    player_2 = Process(target=init_trench_manager, args=('Manager Zach', is_trench_manual, sys.stdin.fileno()))
    player_2.start()

    controller = GameServer()

if __name__ == '__main__':
    main()
