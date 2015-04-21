#encoding:utf-8
'''2015-1-20'''

import networkx as nx
import random
import csv
import os
import sys


class IC_Model: 
    
    def __init__(self,KnowNum):
        self.KnowNum=KnowNum
        print KnowNum
        
        
    def creatGraph(self): 
        file=open('G:/workspace/SIR-IC/src/tmp/network-single-1.edges','rb')
        G = nx.Graph()
        ICedge={}#�ڵ��ţ��ڵ�״̬
        edges=file.readlines()
        for line in edges:
            l=line.split("\t")
            edge=((int(l[0]),int(l[1])))
            G.add_edge(edge[0],edge[1])
        nodes=G.nodes()
        ICedge=dict.fromkeys(nodes, 'u')#initialise the nodes' status to unknow
              
#         degree=G.degree()
#         print degree
        
        return G,ICedge 

    def ThrowNews(self,NBnode,IC,ic_St):
        KnowNum=self.KnowNum
        num=random.random()
        if num < KnowNum and IC[NBnode]=='u':
            IC[NBnode]='k' #the status of node is known
            ic_St.append(NBnode)
    
    def isContinue(self,temp):

        if len(temp)>149:
            return False
        else:
            return True
        
                
    def ICmodel(self):
        graph,ICedge=self.creatGraph()
#         nodes=graph.number_of_nodes() 
#         i=random.randint(0,nodes-1)#initialise the infected
        ICedge[924]='k'
        temp=[]
        ic_St=[]
        ic_St.append(924)
        
        while(self.isContinue(temp)):
            values=ICedge.values()
            u=values.count('u')
            k=values.count('k')
            temp.append((u,k))
            
            if ic_St:
                keys=ic_St[:]
                ic_St=[]
                for key in keys:
                    if ICedge[key]=='k':
                        nb=[]#the neighbours of infected node
                        nb=graph.neighbors(key)
                        for node in nb:
                            self.ThrowNews(node,ICedge,ic_St)
                            
        return temp
    
def IC2Excel(outPath,fileName,newsList):
        
    writer=csv.writer(file(os.path.join(outPath,fileName+".csv"),'a+b'))
    for r in newsList:
        writer.writerow([r[0],r[1]])      
    
    
def average(numlist):
    lennum=len(numlist)#Ҫ������б���
    minrow=len(numlist[0])#�б���С����
#     for list in numlist:
#         if minrow>len(list):
#             minrow=len(list)
    
    temp=[]    
    column=len(numlist[0][0])#�б�����    
    for i in range(minrow):#��
        avenum=[]
        for j in range(column):#������
            sum=0
            for list in numlist:
                sum=sum+(list[i][j])#��i�е�j�е�ֵ���
            columnave=sum/lennum
            avenum.append(columnave)
        temp.append(avenum)
        
    return temp
    
def main():
    
    
    kList=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    outPath="G:/workspace/SIR-IC/result/ICMSingle"
    
    for k in kList:
        ALLresult=[]
        for i in range(100):
            ICM=IC_Model(k)
            result=ICM.ICmodel()
            ALLresult.append(result)
            
        AveResult=average(ALLresult)
        IC2Excel(outPath,'k='+str(k),AveResult)
        
       
if(__name__ == "__main__"):
    main();
