from random import randint
from random import shuffle


def create_map():
    '''
    Function is responsible for creating a pseudo-random world
    '''
    blocks = []
    string = []
    index = []

    for i in range(0, 29, 1):
        blocks.append((0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 3, 3, 4))

    for i in range(0, 28, 1):
        index.append(randint(1, 15))

    blocks[0] = (0,0,0,0,0,1,2,2,2,2,2,2,2,4)
    blocks[1] = (0,0,0,0,0,1,2,2,2,2,3,2,2,4)
    blocks[2] = (0,0,0,0,0,0,1,2,2,3,0,0,0,4)
    blocks[3] = (0,0,0,0,0,1,2,2,2,3,0,0,2,4)

    blocks[4] = [0,0,0,0,0,1,2,2,0,0,0,2,2,4]
    blocks[5] = [0,0,0,0,0,0,1,2,2,2,2,2,3,4]
    blocks[6] = [0,0,0,0,0,0,1,2,3,2,2,2,2,4]

    blocks[7] = [0,0,0,0,0,0,1,2,2,0,0,0,2,4]
    blocks[8] = [0,0,0,0,0,1,2,0,2,2,3,2,0,4]
    blocks[9] = [0,0,0,0,1,2,2,2,0,0,3,3,2,4]

    blocks[10] =[0,0,0,1,2,2,2,2,2,2,2,2,2,4]
    blocks[11] =[0,0,0,0,1,2,2,2,2,2,2,0,3,4]
    blocks[12] =[0,0,0,0,0,1,2,2,2,2,2,2,3,4]

    blocks[13] =[0,0,0,0,0,0,1,2,3,2,3,2,2,4]
    blocks[14] =[0,0,0,0,0,0,1,2,2,3,2,2,2,4]
    blocks[15] =[0,0,0,0,0,0,1,2,2,0,2,2,2,4]

    blocks[16] = (0,0,0,0,0,1,2,0,2,2,2,2,2,4)
    blocks[17] = (0,0,0,0,0,1,0,3,0,2,3,2,2,4)
    blocks[18] = (0,0,0,0,0,0,1,0,0,3,3,2,2,4)
    blocks[19] = (0,0,0,0,0,1,2,2,2,3,2,2,2,4)

    blocks[20] = [0,0,0,0,0,1,2,2,2,2,2,2,2,4]
    blocks[21] = [0,0,0,0,0,0,1,2,2,3,2,2,2,4]
    blocks[22] = [0,0,0,0,0,0,1,2,2,2,2,2,2,4]

    blocks[23] = [0,0,0,0,0,0,1,2,2,2,3,2,2,4]
    blocks[24] = [0,0,0,0,0,1,2,2,2,2,2,3,2,4]
    blocks[25] = [0,0,0,0,1,2,2,2,2,2,2,2,2,4]

    blocks[26] =[0,0,0,1,2,2,2,2,0,0,0,2,2,4]
    blocks[27] =[0,0,0,0,1,2,2,2,0,2,2,2,2,4]
    blocks[28] =[0,0,0,0,0,1,2,2,2,0,0,0,2,4]

    shuffle(blocks)

    for i in range(0, 14, 1):
        strin = ""
        for j in range(0, 29, 1):
            strin = str(strin) + str(blocks[j][i])
            
        string.append(strin)
        strin = 0

    f = open('map_seed.txt', 'w')
    for i in range(0, 14, 1):
        f.write(string[i] + '\n')
    f.close()
