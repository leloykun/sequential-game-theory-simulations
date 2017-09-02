import time
import numpy as np
import matplotlib.pyplot as plt
    
num_data_files = 5
bounds = [i for i in range(100, 150 + 1)]
layers = 2
steps = 10

for depth in range(1, 5):
    start = time.time()
    
    data = [[[0 for layer in range(layers)] for _ in range(11)] for _ in range(11)]
    for i in range(1, num_data_files + 1):
        with open(str(depth) + "/data" + str(i) + ".txt") as f:
            temp = f.readlines()
            for line in temp:
                alpha, gamma, *fed = map(int, line.split())
                for layer in range(layers):
                    data[alpha][gamma][layer] += fed[layer] / num_data_files
    #print(data)
    for layer in range(layers):
        temp = [[0 for _ in range(11)] for _ in range(11)]
        for alpha in range(11):
            for gamma in range(11):
                temp[alpha][gamma] = (data[alpha][gamma][layer] - (data[alpha][gamma][layer-1] if layer > 0 else 0)) / steps
        
        #print(data)
        
        plt.imshow(temp, extent=[-0.5, 10.5,-0.5,10.5], origin='lower', 
                   interpolation='nearest', vmin=0, vmax=200, cmap='Blues') #BrBG
                   
        plt.title("QLearning Parameters vs. Agent Performance\nVisual Depth = "+str(depth)+" || Layer: "+str(layer+1))
        plt.xlabel("Discount Rate")
        plt.ylabel("Learning Rate")
        
        # TODO: make this uniform
        plt.colorbar(boundaries=bounds, spacing='uniform', label='Agent Performance', ticks=[], extend='max')
        plt.tight_layout()
        plt.savefig(str(depth) + "/plot" + str(layer + 1))
        plt.close()
        #plt.show()
        
    print("visual depth", depth, "run time:", time.time() - start)
