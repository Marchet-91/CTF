#! /usr/bin/python3

import random
import os

FLAG = os.environ['FLAG']
PLAYS = 100

HELP = """
This game is a fair & open source heads or tails game where the server cannot cheat you and you cannot cheat the server. You can play at home with a real coin.
First, you toss a coin and hash a phrase containing the result using our hashing function, like "My coin landed on tails !". Your phrase must contain "heads" or "tails".
After sending your hash, the server will ask you to prove that your coin landed on heads/tails.
You will have to send the initial phrase that you hashed, proving that your coin indeed landed on the good side.
""".strip()


def handle():
    print('Welcome to the Heads or Tails game !\nIf you win at least 9/10 games you\'ll win a gift !\n')
    while True:
        choice = input('1.Play\n2.Hash your input\n3.Help\nCTRL+C to exit\n> ')
        if choice == '1':
            play_game()
        elif choice == '2':
            do_hash()
        elif choice == '3':
            print(HELP)
        else:
            break


def play_game():
    result_list = [random.randint(0, 1) for _ in range(PLAYS)]

    for result in result_list:
        play_hash = input("Heads or tails? Send me the hash of your play!\n")

        expected = ['heads', 'tails'][result]
        bad = ['tails', 'heads'][result]

        play_orig = input(
            f"Now, prove me that you did {expected} by sending your play\n")

        if hash_play(play_orig) != play_hash:
            print(f"Hash mismatch.")
            break
        elif not (expected in play_orig) or (bad in play_orig):
            print(f"Play better next time!")
            break
        else:
            print(f"Good job!")
    else:
        print(f"You're good! Here is your flag : {FLAG}")


def do_hash():
    played = input("Send me what you played, I will give you the hash.")
    if 'heads' not in played and 'tails' not in played:
        print("Your play is invalid, but here is your hash: ", end="")
    print(hash_play(played))


def hash_play(play):
    play += 'A'
    while len(play) % 4:
        play += 'B'
    state = [2, 2, 0, 0, 2, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 2, 1, 0, 0, 2, 1]
    for blockStart in range(0, len(play), 4):
        block = play[blockStart:blockStart+4]
        blockSum = ord(block[0])*0x1000000+ord(block[1]) * \
            0x10000+ord(block[2])*0x100+ord(block[3])
        blockState = []
        while blockSum:
            blockState.append(blockSum % 3)
            blockSum //= 3
        while len(blockState) < 21:
            blockState.append(state[(11+5*len(blockState)) % 21])
        for i in range(21):
            state[i] = [[1, 0, 0], [1, 0, 2], [
                2, 2, 1]][blockState[i]][state[i]]
        newState = state[14:21]+state[0:7]+state[7:14]
        for i in range(0, 21, 2):
            state[i] = (state[i]-1) % 3
        for i in range(1, 21, 2):
            state[i] = (state[i]+1) % 3
        for i in range(21):
            state[i] = [[1, 0, 0], [1, 0, 2], [2, 2, 1]][newState[i]][state[i]]
        newState = state[3:6]+state[18:21]+state[12:15] + \
            state[6:9]+state[9:12]+state[0:3]+state[15:18]
        for i in range(21):
            state[i] = ([[1, 0, 0], [1, 0, 2], [2, 2, 1]]
                        [state[i]][newState[i]]+blockState[-i]) % 3
    return ''.join([['O', '0', 'o'][stateElem] for stateElem in state])


if __name__ == "__main__":
    while 1:
        try:
            handle()
        except Exception as e:
            print("You did something wrong!!\n", str(e))
