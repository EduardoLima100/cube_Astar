import pickle
import matplotlib.pyplot as plt

def print_DATA(DATA):
    print("Distância:","\tTempo médio:","\t\t\tOcorrências:")
    for i in range(len(DATA)):
        print(i+1,"\t|\t","%.20f"%DATA[i][0],"\t|\t",DATA[i][1])

try:
    with open('times_data', 'rb') as fp:
        DATA = pickle.load(fp)
        fp.close()
except IOError:
    print("Não há dados")
    
if(len(DATA)>0):
    DT = []
    for i in range(len(DATA)):
        if DATA[i][1] > 50:
            DT.append(DATA[i])
    
    X = range(1,len(DT)+1)
    Y = []
    for y in DT:
        Y.append(y[0])
    
    print_DATA(DT)
    
    plt.rcParams['figure.figsize'] = (7,7)
    plt.plot(X,Y)
    plt.grid()
    plt.show()

        
