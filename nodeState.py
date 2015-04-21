#encoding:utf-8
'''2014-12-29
统计不同社团不同状态的节点数目变化
@author Nikita'''


import csv
import os

class Dataprocess:
    
    def __init__(self,rateNum,outPath,fileName):
        self.rateNum=rateNum
        self.outpath=outPath
        self.fileName=fileName
        print rateNum
    
    
    def getCommunityStates(self,community):
        comNumList=[20,11,22,36,34,23,28,32,7,2,8,17,18,42,38,40,5,25,45,47,29,14,24,41,37,12,27,15,4,44,46,31,43,35,3,19,1,16,26,6,33,13,9,10,21,39,30]
        #the community number with the community size Ascending order
        CommuAveStates=[]#the average infected rates each time of all community 
        for comNum in comNumList: 
            rStatelist=[]    #infected rate each iteration of a community 
            for j in range(0,100):
                comNodeStates=[]#all nodes status each iteration of a community 
                InfeNodelist=[]#the rate of infected individuals in a community 
                for node in range(0,1000):
                    if community[node][1]==comNum:
                        nodestate=self.getNodestates(node,j)
                        comNodeStates.append(nodestate)
                        
                InfeNodelist=self.countInfeNode(comNodeStates)    
                rStatelist.append(InfeNodelist)#[100*150]
                    
#             self.list2excel(self.outpath, 'community'+str(comNum), rStatelist)
            CommuAveStates.append(self.cmmuInfeAverage(rStatelist))#all communitys' average data-recovered rate
        self.list2excel(self.outpath, 'commuAveRecover', CommuAveStates)
        self.fina_res2txt(CommuAveStates)   
        
    def Count_infeRate(self): 
        
        
    def getNodestates(self,node,j):
        fileName=self.fileName+str(j)
        filepath='G:/workspace/SIR-IC/result/k='+str(self.rateNum[1])+'i='+str(self.rateNum[0])+'r=0.2'
        nodestate=csv.reader(file(os.path.join(filepath,fileName+".csv"),'r'))
        nodelist=[]
        for nodes in nodestate:
            nodelist.append(nodes[node])
        
        return nodelist# 150 states of a node 
    
    
    def countInfeNode(self,nodelist):#accumulate State
        communitystate=[]#the rate of infected individuals in a community 
        communitySize=len(nodelist)
        for j in range(0,150):
            timelist=[]
            for i in range(0,communitySize):
                timelist.append(nodelist[i][j])
                
            i=timelist.count('i')
            r=timelist.count('r')
            I=i+r
            communitystate.append(float(I)/float(communitySize))#
            
#         if communitystate.count(0.0)>148:#疾病没有传播开
#             return 0
#         else:
#             return communitystate
        return communitystate
    
    def list2excel(self,outPath,fileName,newsList):
        writer=csv.writer(file(os.path.join(outPath,fileName+".csv"),'a+b'))
        for row in newsList:
            writer.writerow([s for s in row])    
            
    def fina_res2txt(self,resultList):
        file_Com=open('community_InfRate.txt','a') 
        for row in resultList:
            file_Com.write(str(row[-1])+'\t') 
        file_Com.write('\n')
        file_Com.close()

    def cmmuInfeAverage(self,Infelist):
        row=len(Infelist)
        colum=len(Infelist[0])
        temp=[]
        
        for c in range(0,colum):
            sum_all=0
            for r in range(0,row):
                sum_all=sum_all+Infelist[r][c]
            avenum=sum_all/float(row)
            temp.append(avenum)
        return temp
    
 
    
    def readCommunityFile(self):
        fileC=open('G:/workspace/SIR-IC/src/tmp/community-1.dat','rb')
        community=[]
        for line in fileC.readlines():
            l=line.split("\t")
            community.append((int(l[0]),int(l[1]),int(l[2])))#get the community
        return community  
     
    def run(self):
        
#         fileName='StSIRState'
#         kList=[0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#         iList=[0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#         community=self.readCommunityFile()
#         for i in iList:#information spread rate
#             for k in kList:#infected rate
#                 rateNum=[]
#                 rateNum.append(i)
#                 rateNum.append(k)
#                 outPath="G:/workspace/SIR-IC/result/communityStates/k="+str(rateNum[1])+"i="+str(rateNum[0])+"r=0.2"
#                 os.makedirs(outPath)
#                 datapro=Dataprocess(rateNum,outPath,fileName)
#                 datapro.getCommunityStates(community)
        
    
if(__name__ == "__main__"):
    
    run();
        
    
