import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def visualize(runs=10):
    for run in range(1, runs + 1):
        data = [[], [], [], []]
        time = []
        
        with open('data/dist/' + str(run) + 'run.txt') as f:
            for line in f.readlines():
                a, b, c, d = map(int, line.split())
                time.append(len(time) + 1)
                data[0].append(a)
                data[1].append(b)
                data[2].append(c)
                data[3].append(d)
        
        '''with sns.color_palette("PuBuGn_d"):
            for i in range(4):
                # sns.tsplot(data=data[i])
                plt.plot(time, data[i])'''
                
        fig, ax = plt.subplots()
        
        plt.xlim(1, 1000)
        plt.ylim(1, 50)
        
        time = np.array(time)
        for i in range(4):
            sns.regplot(x=time[:1000], y=np.array(data[i][:1000]), ax=ax, ci=100, marker="+", n_boot=10000, scatter=False)
        
        plt.savefig('data/dist/' + str(run) + 'plot1K')
        plt.close()
        print("done with run %d" % run)

if __name__ == '__main__':
    visualize()