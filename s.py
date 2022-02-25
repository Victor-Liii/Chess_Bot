import matplotlib.pyplot as plt
import random 

wins =[]
def end(nc):
    for i in range(len(nc)): 
        if nc[i] == 0:
            return i
    
    return -1

for i in range(1):
    np = 5 #number of players
    nc = [] #number of cards lef
    acc = []
    sd = 20 #starting deck
    ns = 10 # number of simulations
    record = []
    counter = 0
    for i in range(np):
        nc.append(sd)
        acc.append(0)
        record.append([])
    
    def clear(acc,nc,j):
        for i in range(len(acc)):
            nc[j] += acc[i]
            acc[i] = 0

    while True:
        for j in range(len(nc)):
            nc[j] -= 1
            acc[j] +=1
            target = random.randint(1,np)-1
            if(random.random()<0.1):
                clear(acc,nc,j)
            if random.random()<0.2 and j!= 0:
                if(random.random()<0.5):
                    nc[target] += acc[j]+acc[target]
                    acc[j] = 0
                    acc[target] = 0
                else: 
                    nc[j] += acc[target] + acc[j]
                    acc[target] = 0
                    acc[j] = 0
            if nc[j] == 0 and acc[j] !=0:
                nc[j] = acc[j]
                acc[j] = 0


        for i in range(len(nc)):
            record[i].append(nc[i]+acc[i])
        counter +=1

        if(counter >500):
            break
        
        a = end(nc)
        if a != -1:
            wins.append(a)
            break

print(wins)
for i in range(len(record)):
    plt.plot(record[i],label = i)

plt.legend()
plt.show()





