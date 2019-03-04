import processor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#fixed input
#arr=np.array([[1,1],[1,2],[1,3],[4,1],[5,1],[0,0],[6,1],[5,5],[5,6],[6,5]])

#read input from csv
#df = pd.read_csv('../clustering_benchmark_1.csv')
#arr = np.concatenate( (np.array(df['x']).reshape(df['x'].size,1), np.array(df['y']).reshape(df['y'].size,1)), axis=1)

#custom built dataset from sklearn
from sklearn import datasets

arr, y = datasets.make_circles(n_samples=500, factor=0.74, noise=0)
#arr, y = datasets.make_blobs(n_samples=50)
#end of custom dataset

e=0.2
minPoint=2


clusterInfo = np.empty(arr.shape[0])
#create a core node info list
coreNodeInfo = []
#0 = not visited, -1 = outlier, >0 = cluster number
clusterInfo.fill(-1)    

#sample nodes at random
randomPointQueue = np.random.choice(arr.shape[0], size=arr.shape[0], replace=False)
randomPointQueue = randomPointQueue.tolist()
#start cluster number from 1
clusterNum = 1

def findAllCoreNode(arr, e, minPoint):
    global randomPointQueue
    global coreNodeInfo
    for ind in range(len(arr)):
        ind_lst = processor.findNeighbor(arr[ind], arr, e)
        if len(ind_lst) >= minPoint:
            coreNodeInfo.append(1)
        else:
            coreNodeInfo.append(0)   

def findCluster(i, arr, e, minPoint):
    global clusterNum, randomPointQueue
    ind_lst = processor.findNeighbor(arr[i], arr, e)
    ind_lst = ind_lst.tolist()
    for tmp in ind_lst:
        if tmp==i: ind_lst.remove(tmp)
    clusterInfo[i]=clusterNum
    clusterInfo[ind_lst]=clusterNum
    
    while len(ind_lst)!=0:
        ind=ind_lst.pop(0)
        if coreNodeInfo[ind]==1:
            #remove from stack
            if ind in randomPointQueue:
                randomPointQueue.remove(ind)
                lst = processor.findNeighbor(arr[ind], arr, e)
                lst = lst.tolist()
                for tmp in lst:
                    if tmp==ind: lst.remove(tmp)
                clusterInfo[ind]=clusterNum
                clusterInfo[lst]=clusterNum
                for l in lst:
                    if l not in ind_lst:
                        ind_lst.append(l)
    clusterNum+=1
        
def runDbscan(arr, e, minPoint):
    global coreNodeInfo, randomPointQueue
    findAllCoreNode(arr, e, minPoint)
    while len(randomPointQueue)!=0:
        ind = randomPointQueue.pop(0)
        if coreNodeInfo[ind]==1:
            findCluster(ind, arr, e, minPoint)

#run the main code
runDbscan(arr, e, minPoint)   

#display number of clusters found
print("Number of cluster detected: ",clusterNum-1)  

df = pd.DataFrame()
df['x'] = arr[:,0]
df['y'] = arr[:,1]
df['clusterInfo'] = clusterInfo

plt.scatter(df['x'][clusterInfo==-1], df['y'][clusterInfo==-1], s=20, marker='*', c='black')
plt.scatter(df['x'][clusterInfo!=-1], df['y'][clusterInfo!=-1], marker='o', c=clusterInfo[clusterInfo!=-1])
