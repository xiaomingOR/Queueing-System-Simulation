import numpy as np
import queue
import copy
import matplotlib.pyplot as plt

qu1 = queue.Queue() 
qu1.put(1)
qu1.get()
qu1.put(2)
for item in list(qu1.queue):
    print(item)