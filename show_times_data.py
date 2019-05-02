import pickle
import matplotlib.pyplot as plt

def print_DATA(DATA):
    print("Distância:","\tTempo médio:","\t\t\tOcorrências:")
    for i in range(len(DATA)):
        print(DATA[i][0],"\t|\t","%.20f"%DATA[i][1],"\t|\t",DATA[i][2])
try:
    with open('times_data', 'rb') as fp:
        DATA = pickle.load(fp)
        fp.close()
except IOError:
    print("Não há dados")
    
if(len(DATA)>0):
    DT = []
    for i in range(len(DATA)):
        DT.append([i]+DATA[i])
    
    i = 0
    while i < len(DT):
        if DT[i][2] < 50:
            DT.remove(DT[i])
        else:
            i=i+1
    
    print_DATA(DT)
    
    X = []
    for x in DT:
        X.append(x[0])
    Y = []
    for y in DT:
        Y.append(y[1])
    
    
    
    plt.rcParams['figure.figsize'] = (7,7)
    plt.plot(X,Y)
    plt.grid()
    plt.show()

        
