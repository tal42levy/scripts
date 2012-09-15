colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'red']


motions = [[0,0], [1,0]]

sensor_right = 0.8

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

total = len(colors) * len(colors[0])
n = 1.0 / total
p = [[n, n, n, n, n],
     [n, n, n, n, n],
     [n, n, n, n, n],
     [n, n, n, n, n]]

def makeMove(motion):
    temp = []
    for i in range(len(p)):
        temp.append([])
        for j in range(len(p[0])):
            y = ((i - motion[0]) % len(p))
            x = ((j - motion[1]) % len(p[0]))
            #print "p[" + str(y) + "][" + str(x) + "] = " + str(p[y][x])
            temp[i].append((1 - p_move) * p[i][j] + p_move *  p[y][x])
    return temp

def sense(measurement):
    q = [];
    for i in range(len(p)):
        q.append([]);
        for j in range(len(p[0])):
            hit = (colors[i][j] == measurement)
            n = p[i][j] * (hit * sensor_right + (1 - hit) * (1 - sensor_right))
            q[i].append(n)
    qsum = []
    for i in range(len(q)):
        qsum.append(sum(q[i]))
    s = sum(qsum)
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] = q[i][j] / s
    return q
    
for i in range(len(motions)):
    p = makeMove(motions[i])
    p = sense(measurements[i])

show(p)



#Your probability array must be printed 
#with the following code.

show(p)




