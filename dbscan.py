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

#arr, y = datasets.make_moons(n_samples=500, factor=0.74, noise=0.15)
arr, y = datasets.make_blobs(n_samples=500)
#end of custom dataset

e=2
minPoint=3

#arr = system.args[2]
#generate queue of random selection
randomPointQueue = np.random.choice(arr.shape[0], size=arr.shape[0], replace=False)
randomPointQueue = randomPointQueue.tolist()
#create a visited list
clusterInfo = np.empty(arr.shape[0])
#0 = not visited, -1 = outlier, >0 = cluster number
clusterInfo.fill(0)    

#start cluster number from 1
clusterNum = 1


def isCoreNode(i, arr, e, minPoint):
    global clusterNum
    #define the stack for neighbor searching using dfs
    customQueueArr = []
    ind_lst = processor.findDistance(arr[i], arr, e)
    print(len(ind_lst))
    #not core node
    if len(ind_lst)<minPoint and clusterInfo[i]<1: #clusterInfo[i]<1 makes sure classified nodes aren't affected
        clusterInfo[i]=-1
        
    #if core node 
    elif len(ind_lst)>=minPoint:
        tmpArr=[]
        clusterInfo[i]=clusterNum
        clusterInfo[ind_lst]=clusterNum
        for ind in ind_lst:
            #remove from global random sample list
            if ind in randomPointQueue:
                randomPointQueue.remove(ind)
                #remove from stack
                if ind in customQueueArr: customQueueArr.remove(ind)
                #ignore current node
                if ind != i:    tmpArr+=ind
        customQueueArr = np.append(tmpArr, customQueueArr).tolist()
        
    while len(customQueueArr)!=0:
        ind = customQueueArr[0]
        customQueueArr = customQueueArr[1:]
        isCoreNode(ind, arr, e, minPoint)
    clusterNum+=1
        
def runDbscan(arr, e, minPoint):
    global randomPointQueue
    while len(randomPointQueue)!=0:
        ind = randomPointQueue[0]
        randomPointQueue = randomPointQueue[1:]  
        isCoreNode(ind, arr, e, minPoint)

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
