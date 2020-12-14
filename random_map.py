from random import randint
from random import shuffle
blocks = []
string = []
index = []

for  i in range(0,29, 1):
    blocks.append((0,0,0,0,0,1,2,2,2,2,2,3,3,4))

for i in range(0,28,1):
    index.append(randint(1,15)) 



blocks[0] = (0,0,0,0,0,1,2,2,2,2,2,3,3,4)    
blocks[1] = (0,0,0,0,0,1,2,2,2,2,2,3,3,4)
blocks[2] = (0,0,0,0,0,0,1,2,2,3,2,3,3,4)
blocks[3] = (0,0,0,0,0,1,2,2,2,3,2,3,3,4)

blocks[4] = [0,0,0,0,0,1,2,2,2,3,2,3,3,4]
blocks[5] = [0,0,0,0,0,0,1,2,2,2,2,3,3,4]
blocks[6] = [0,0,0,0,0,0,1,2,2,2,3,3,3,4]

blocks[7] = [0,0,0,0,0,0,1,2,2,2,3,3,3,4]
blocks[8] = [0,0,0,0,0,1,2,2,2,2,3,3,3,4]
blocks[9] = [0,0,0,0,1,2,2,2,2,2,3,3,3,4]

blocks[10] = [0,0,0,1,2,2,2,2,2,2,2,3,3,4]
blocks[11] = [0,0,0,0,1,2,2,2,2,2,2,3,3,4]
blocks[12] = [0,0,0,0,0,1,2,2,3,2,2,3,3,4]

blocks[13] = [0,0,0,0,0,0,1,2,3,3,3,3,3,4]
blocks[14] = [0,0,0,0,0,0,1,2,2,3,3,3,3,4]
blocks[15] = [0,0,0,0,0,0,1,2,2,3,3,3,3,4]

shuffle(blocks)

for i in range(0,14,1):
    strin = blocks[0][0]
    for j in range(0,29,1):
        strin = str(strin) + str(blocks[j][i])
        
    string.append(strin)
    strin = 0

f = open('map_seed.txt', 'w')
for i in range(0,14,1):
    f.write(string[i] + '\n')
f.close()


print(blocks)
print(index)
print(len(index))
print(string)















