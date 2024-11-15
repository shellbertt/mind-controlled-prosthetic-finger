import matplotlib.pyplot as plt
import random
import time
 
plt.ion()  # turning interactive mode on
graph = plt.plot([], [])[0]
plt.pause(1)
for i in range(10):
    time.sleep(1)
    # removing the older graph
    graph.remove()

    # updating the data
    y = [random.randint(1,10) for i in range(20)]
    x = [*range(1,21)]
     
    # plotting newer graph
    graph = plt.plot(x,y,color = 'g')[0]
     
    # calling pause function for 0.25 seconds
    plt.pause(0.25)
