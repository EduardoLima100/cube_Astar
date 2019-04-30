import pickle

global DATA

def print_DATA():
    print("Distância:","\tTempo médio:","\t\t\tOcorrências:")
    for i in range(1,len(DATA)):
        print(i,"\t|\t","%.20f"%DATA[i][0],"\t|\t",DATA[i][1])

try:
    with open('times_data', 'rb') as fp:
        DATA = pickle.load(fp)
        fp.close()
        print_DATA()
except IOError:
    print("Não há dados")
    


        
