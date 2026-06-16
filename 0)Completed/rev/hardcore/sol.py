import hashlib
import random
import sys
from string import printable

FLAG_LEN = 62

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

def main(flagbuf):
    print(flagbuf)
    
    bank = set(load_bank()) 

    # for _ in range(FLAG_LEN):
    #     # sys.stdout.write(random.choice(DIALOGUES))
    #     # sys.stdout.flush()

    #     # try:
    #     #     # Take input and grab the first character
    #     #     # user_input = input()
    #     #     if not user_input:
    #     #         raise ValueError
    #     #     char = user_input[0]
    #     # except (EOFError, ValueError):
    #     #     print("There has to be some way to talk to this person, you just haven't found it yet.")
    #     #     return

    tmp_hash = hashlib.md5(flagbuf).digest()
    # Bank hit = FAIL
    if tmp_hash in bank:
        return "There has to be some way to talk to this person, you just haven't found it yet."

    return "Hey it looks like you have input the right flag. Why are you still here?"

bank = set(load_bank()) 

fringe = [b""]
while True:
    for i in fringe: 
        if len(i) == 62:
            print(i)
            break

    new_fringe = []
    for f in fringe: 
        for c in printable:
            tmp = f + c.encode()
            if hashlib.md5(tmp).digest() not in bank:
                new_fringe.append(tmp)
    fringe = new_fringe
        
    
bfs()      

# for c in printable:
#     if "There has to be some way to talk to this person, you just haven't found it yet." in main(c):
#         print(c)



# flag = b"srdnlen{"
# tested = {}
# i = -1

# while True:
#     i += 1
#     if tested.get(i, 0) == 0:
#         tested[i] = ""
#     for c in printable:
#         if c in tested[i]:
#             continue
#         tmp = flag + c.encode()
#         if not "There has to be some way to talk to this person, you just haven't found it yet." in main(tmp):
#             flag += c.encode()
#             print("flag", flag)
#             break
#     else:
#         i -= 2
#         tested[i + 1] += flag[i + 1]
#         flag = flag[:-1]
#     # print(flag)