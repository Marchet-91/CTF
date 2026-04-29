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

alpha = "ABCEFGHIJKLMNOPQRSTUVWXYZ"
diz = {}
def searchT(diz):
    for first in alpha:
        # print(first)
        for second in alpha:
            for third in alpha:
                test = "tails" + first + second + third
                hash1 = hash_play(test)
                if diz.get(hash1, 0) != 0:
                    return test, diz[hash1]

for first in alpha:
    # print(first)
    for second in alpha:
        for third in alpha:
            test = "heads" + first + second + third
            diz[hash_play(test)] = test

find, t = searchT(diz)

print(find, t)
print(find, hash_play(find))