import hashlib
import random
import sys

FLAG_LEN = 62
DIALOGUES = [
    "HARDCORE!\n",
    "HARDCORE TO THE MEGA!\n",
    "HAAAAARD COOOOORE!\n",
    "Internally Coherent!\n",
    "YEEEEEEEEEEAHHHHHHHH!\n",
    "Is it though?\n",
    "The question is, what is the question?\n",
    "HARD CORE! ALL RIGHT! YEAH!\n",
    "SO HARD CORE!\n",
    "But is it? I mean, really?\n",
    "Good morning yeah! One two three! Yekokata, the place to be!\n",
    "CRAB MAN!\n",
    "Lakierski Materialski!\n",
    "LOVE IS HARDCORE!\n",
    "Spinning out lyrics since the day I was born!\n",
    "And the amount of lyrics I got is against the law!\n",
]

def load_bank(filename="hardcore.bnk"):
    bank_list = []
    try:
        with open(filename, "rb") as f:
            # Read MD5 hashes 16 bytes at a time
            while chunk := f.read(16):
                if len(chunk) == 16:
                    bank_list.append(chunk)
    except FileNotFoundError:
        print("Error: hardcore.bnk not found.")
        sys.exit(1)
    return bank_list

def main():
    
    bank = set(load_bank()) 
    flagbuf = ""

    for _ in range(FLAG_LEN):
        sys.stdout.write(random.choice(DIALOGUES))
        sys.stdout.flush()

        try:
            # Take input and grab the first character
            user_input = input()
            if not user_input:
                raise ValueError
            char = user_input[0]
        except (EOFError, ValueError):
            print("There has to be some way to talk to this person, you just haven't found it yet.")
            return

        flagbuf += char
        tmp_hash = hashlib.md5(flagbuf.encode("ascii")).digest()

        # Bank hit = FAIL
        if tmp_hash in bank:
            print("There has to be some way to talk to this person, you just haven't found it yet.")
            return

    print("Hey it looks like you have input the right flag. Why are you still here?")

if __name__ == "__main__":
    main()
