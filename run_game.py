import sys
import os

def main():
<<<<<<< HEAD
<<<<<<< Updated upstream
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
=======
    # tbd
    '''
        This is for us to streamline the execution of this game
        For now, please use submarine_server.py directly.
    '''
    pass
>>>>>>> Stashed changes
=======
    # tbd
    '''
        This is for us to streamline the execution of this game
    '''
    pass
>>>>>>> 7a7068a355d096511d32d1e536cbc53a2a2b8295

if __name__ == '__main__':
    main()
