#encoding:utf-8

'''created at 2014-9-12
 desease and information spreading 
new function for me :networkx.graph/random()
@author Nikita
'''


import networkx as nx
import random
import math
import csv
import os
import sys

class IC_Model: #IC information spreading network
    
    def creatGraph(self): 
        file1=open('G:/workspace/SIR-IC/src/tmp/network-single-1.edges','rb')
        G = nx.Graph()#the IC network
#         iCedge={}
        edges=file1.readlines()
        for line in edges:
            l=line.split("\t")
            edge=((int(l[0]),int(l[1])))
            G.add_edge(edge[0],edge[1])
        nodes=G.nodes()
        iCedge=dict.fromkeys(nodes, 'u')#initialise all the nodes' status to unknow
                   
        return G,iCedge 

    def ThrowNews(self,NBnode,IC,ic_St,rateNum):
        KnowNum=rateNum[1]
        num=random.random()
        if num < KnowNum and IC[NBnode]=='u':
            IC[NBnode]='k' #the status of node is known
            ic_St.append(NBnode)
            
    def ICmodel(self,ICedge,graph,ic_St,rateNum):
        if ic_St:
            keys=ic_St[:]
            ic_St=[]
            for key in keys:
                if ICedge[key]=='k':
                    nb=[]#the neighbours of infected node
                    nb=graph.neighbors(key)
                    for node in nb:
                        self.ThrowNews(node,ICedge,ic_St,rateNum)
        return ICedge,ic_St
    
    
class SIR_Model:#disease spreading network
    def __init__(self,rateNum,stepLengh):
        self.rateNum=rateNum
        self.stepLengh=stepLengh
        print rateNum
    
    def creatGraph(self):
        file1=open('G:/workspace/SIR-IC/src/tmp/network-1.edges','rb')
        G = nx.Graph()
        edges=file1.readlines()
        for line in edges:
            l=line.split("\t")
            edge=((int(l[0]),int(l[1])))
            G.add_edge(edge[0],edge[1])
        nodes=G.nodes()
        SIR=dict.fromkeys(nodes, 's')#initialise the nodes' status to susceptible 
        return G,SIR
     
    def isContinue(self,temp):
        if len(temp)>self.stepLengh:
            return False
        else:
            return True
        
        
    def SIRinfect(self,NBnode,SIR,sens):#the single diseases Spreading 
        i=self.rateNum[0]#the infection rate
        num=random.random()
        if num < i and SIR[NBnode]=='s':
            SIR[NBnode]='i'
            sens.append(NBnode)
                
    def getcommunity(self):
        file2=open('G:/workspace/SIR-IC/src/tmp/community-1.dat','rb')
        comuList=[]
        for line in file2.readlines():
            l=line.split("\t")
            comuList.append((int(l[0]),int(l[1]),int(l[2])))
        return comuList  
                    
    def SIRICinfect(self,NBnode,SIR,sens,ic,ic_st,comuList):
        i=self.rateNum[0] #
        if ic[NBnode]=='u'and SIR[NBnode]=='s':#the individuals unknown the diseases information 
            num=random.random()
            if num < i :
                SIR[NBnode]='i'
                sens.append(NBnode)
                if ic:
                    ic[NBnode]='k'#the infected node get the diseases information automatically 
                    ic_st.append(NBnode)
        else:
            if ic[NBnode]=='k' and SIR[NBnode]=='s':
                num=-2*(comuList[NBnode][2])/96.0 #normalization
                infNum=i*(1-math.exp(num))
                rannum=random.random()
                if rannum < infNum :
                    SIR[NBnode]='i'
                    sens.append(NBnode)
                 
                                    
    def recoverNeib(self,NBnode,SIR,sir_St):
        recoverRate=self.rateNum[2]
        num=random.random()
        if num<recoverRate and SIR[NBnode]=='i':
            SIR[NBnode]='r'
            sir_St.remove(NBnode)
      
    def SIRmodel(self):#disease single spreading
        sir_St=[]
        temp=[]
        graph,sir=self.creatGraph()
        nodes=graph.number_of_nodes() 
        i=random.randint(0,nodes-1)#initialise the seed 
        sir[i]='i'
        sir_St.append(i)
        
        StState=[]#the all nodes' status each iteration 
        while(self.isContinue(temp)):
            values=sir.values()
            StState.append(values)
            s=values.count('s')
            i=values.count('i')
            r=values.count('r')
            temp.append((s,i,r))
            sens=[]#the infected nodes of each iteration 
            for key in sir_St:
                nb=[]#the neighbours of infected node
                nb=graph.neighbors(key)
                for node in nb:
                    self.SIRinfect(node,sir,sens)
                self.recoverNeib(key,sir,sir_St)
            if sens:
                sir_St.extend(sens)
            
        return temp,StState
    
    
    def SIR_ICmodel(self):#disease spreading with the information spreading
        comuList=self.getcommunity()
        
        graph,sir=self.creatGraph()
        nodes=graph.number_of_nodes() 
        i=random.randint(0,nodes-1)#initialise the seed 
        sir[i]='i'
        sir_St=[]#the infected individuals of the network 
        temp=[]#the numbers of three status 
        sir_St.append(i)
        
        IC=IC_Model()
        ic_St=[]#the known individuals of IC network 
        ICnum=[]#the numbers of three status 
        ICgraph,ICedge=IC.creatGraph()
        ICedge[i]='k'
        ic_St.append(i)
        
        StSIRState=[]#the numbers of three status of each iteration in diseases Network 
        while(self.isContinue(temp)):
            values=ICedge.values()
            u=values.count('u')
            k=values.count('k')
            ICnum.append((u,k))
            ICedge,ic_St=IC.ICmodel(ICedge, ICgraph,ic_St,self.rateNum)
            
            values=sir.values()
            StSIRState.append(values)
            s=values.count('s')
            i=values.count('i')
            r=values.count('r')
            temp.append((s,i,r))
            sens=[]
            for key in sir_St:
                nb=[]#the neighbours of infected node
                nb=graph.neighbors(key)
                for node in nb:
                    self.SIRICinfect(node,sir,sens,ICedge,ic_St,comuList)
                self.recoverNeib(key,sir,sir_St)
            if sens:
                sir_St.extend(sens)  
            
        return temp,ICnum,StSIRState
              
    def SIR2Excel(self,outPath,fileName,newsList):
        try:
            writer=csv.writer(file(os.path.join(outPath,fileName+".csv"),'a+b'))
            for r in newsList:
                writer.writerow([r[0],r[1],r[2],])      
    
        except Exception:
                s=sys.exc_info()
                msg = (u"Output2Excel Error %s happened on line %d" % (s[1],s[2].tb_lineno))
                print msg
                
    def StState2Excel(self,outPath,fileName,newsList):
        try:
            writer=csv.writer(file(os.path.join(outPath,fileName+".csv"),'a+b'))

            for row in newsList:
                writer.writerow([s for s in row])      
    
        except Exception:
                s=sys.exc_info()
                msg = (u"Output2Excel Error %s happened on line %d" % (s[1],s[2].tb_lineno))
                print msg
                
    def IC2Excel(self,outPath,fileName,newsList):
        try:
            writer=csv.writer(file(os.path.join(outPath,fileName+".csv"),'a+b'))
            for r in newsList:
                writer.writerow([r[0],r[1],])      
    
        except Exception:
                s=sys.exc_info()
                msg = (u"Output2Excel Error %s happened on line %d" % (s[1],s[2].tb_lineno))
                print msg
    
def average(numlist):#the average results of 100 times 
    lennum=len(numlist)
    minrow=len(numlist[0])
#     for l in numlist:
#         if minrow>len(l):
#             minrow=len(l)
    temp=[]    
    column=len(numlist[0][0])
    for i in range(minrow):
        avenum=[]
        for j in range(column):
            sum_value =0
            for per_list in numlist:
                sum_value=sum_value+(per_list[i][j])
            columnave=sum_value/lennum
            avenum.append(columnave)
        temp.append(avenum)
    return temp
    
def run(rateNum):
    stepLengh=149
    SIRmodel=SIR_Model(rateNum,stepLengh)
    outpath="G:/workspace/SIR-IC/result/k="+str(rateNum[1])+"i="+str(rateNum[0])+"r=0.2"
    os.makedirs(outpath)
    
    temp=[] #single diseases Spreading 
    for i in range(100):
        temp1,StState=SIRmodel.SIRmodel()
#         SIRmodel.SIR2Excel(outpath,'SIR'+str(i),temp1)
        SIRmodel.StState2Excel(outpath,'StState'+str(i),StState)
        temp.append(temp1)
    avetemp=average(temp)#
    SIRmodel.SIR2Excel(outpath,'SIRAve',avetemp)
         
    SCtemp=[]
    Ictemp=[]
    for i in range(100):
        temp2,ICnum,StSIRState=SIRmodel.SIR_ICmodel()
#         SIRmodel.SIR2Excel(outpath, 'SIR-IC'+str(i), temp2)
#         SIRmodel.IC2Excel(outpath,'IC'+str(i), ICnum)
        SIRmodel.StState2Excel(outpath,'StSIRState'+str(i),StSIRState)
        SCtemp.append(temp2)
        Ictemp.append(ICnum)    
    aveSCtemp=average(SCtemp)
    SIRmodel.SIR2Excel(outpath, 'SIR-ICAve', aveSCtemp)
    file_num =open('finalstatusbumber.txt','a')
    file_num.write(str(aveSCtemp[-1][0])+'\t'+str(aveSCtemp[-1][1])+'\t'+str(aveSCtemp[-1][2])+'\n')
    file_num.close()
    
    aveIctemp=average(Ictemp)
    SIRmodel.IC2Excel(outpath,'ICAve', aveIctemp)
                    
    
def main():
    rec_rate=0.2 #the infected node transform to recovered status
    kList=[0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    iList=[0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    for k in kList:#infected rate
        for i in iList:#active rate
            rateNum=[]
            rateNum.append(i)
            rateNum.append(k)
            rateNum.append(rec_rate)
            run(rateNum)
    
     
    
if(__name__ == "__main__"):
    main();
