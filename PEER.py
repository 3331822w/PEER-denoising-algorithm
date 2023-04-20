# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 08:53:50 2021

@author: Lgkgroup
"""
from __future__ import division
import os
import time
import numpy as np
import copy




def distance_Reciprocal(a,b):
    d_all=a**2+b**2
    d=d_all**0.5
    d=1/d
    return d

def weight_result(data,c):
    m = (c-1)//2
    n=len(data)
    new_data= [0 for x in range(n)]
    for i in range(0,n):
        w_sum=0
        if i <= m - 1:
            lx = 0
            ly = i + m
            p_sum=0
            w_sum=w_sum+data[0]*(m-i)
            a=0
            happens = [0 for x in range(ly-lx+1)]
            for j in range(lx,ly+1):
                w_sum=w_sum+data[j]
            avg=w_sum/c
            if avg in data[lx:ly+1]:
                new_data[i]=avg
            else:  
                for k in range(lx,ly+1):
                    p_sum=p_sum+distance_Reciprocal(data[k],avg)
                for k in range (lx,ly+1):
                    happens[a]=data[k]*(distance_Reciprocal(data[k],avg)/p_sum)
                    new_data[i]=new_data[i]+happens[a]
                    a=a+1
        elif i >= n - m:
            lx = i - m
            ly = n-1
            p_sum=0
            w_sum=w_sum+data[n-1]*(m-n+i)
            a=0
            happens = [0 for x in range(ly-lx+1)]
            for j in range(lx,ly+1):
                w_sum=w_sum+data[j]
            avg=w_sum/c
            if avg in data[lx:ly+1]:
                new_data[i]=avg
            else:  
                for k in range (lx,ly+1):
                    p_sum=p_sum+distance_Reciprocal(data[k],avg)
                for k in range (lx,ly+1):
                    happens[a]=data[k]*(distance_Reciprocal(data[k],avg)/p_sum)
                    new_data[i]=new_data[i]+happens[a]
                    a=a+1
        else:
            lx = i - m
            ly = i + m
            p_sum=0 
            happens = [0 for x in range(ly-lx+1)]
            a=0
            for j in range(lx,ly+1):
                w_sum=w_sum+data[j]
            avg=w_sum/c
            if avg in data[lx:ly+1]:
                new_data[i]=avg
            else:  
                for k in range (lx,ly+1):
                    p_sum=p_sum+distance_Reciprocal(data[k],avg)
                for k in range (lx,ly+1):
                    happens[a]=data[k]*(distance_Reciprocal(data[k],avg)/p_sum)
                    new_data[i]=new_data[i]+happens[a]
                    a=a+1
    return new_data

def derivative(data):
    result = [data[i] - data[i - 1] for i in range(1, len(data))]
    result.insert(0, result[0])
    result2= [result[i] - result[i - 1] for i in range(1, len(result))]

    return result,result2

def move_average(data, weight):
    k = len(weight)
    if k == 0:
        return data
    m = (k - 1) // 2
    orign = data
    n = len(orign)
    result = []
    for i in range(0, n):
        lx = 0
        ly = 0
        if i <= m - 1:
            lx = 0
            ly = i + m
        elif i >= n - m:
            lx = i - m
            ly = n
        else:
            lx = i - m
            ly = i + m
        sum_y = 0
        if i <= m - 1:
            for k in range(m - i):
                sum_y += orign[0] * weight[k]
        elif i >= n - m:
            for k in range(m - n + i + 1):
                sum_y += orign[n - 1] * weight[n - i + k + m]

        for j in range(lx, ly):
            sum_y += orign[j] * weight[j - i + m]
        average_y = sum_y
        result.append(average_y)
    return result

def find_extreme(data,d_data,d2_data):
    big = []
    small=[]
    big_mis=[]
    data_temp=copy.deepcopy(data)
    for i in range(len(d_data) - 1):
        if (d_data[i] < 0 and d_data[i + 1] > 0) :
            small.append(i)
    for i in range(len(small) - 1):
        for j in range(small[i], small[i + 1]):
            if (d_data[j] > 0 and d_data[j + 1] < 0):
                big.append([[small[i], small[i + 1]], j])
    print(big)
    #print('---------------')
    big_premis=[]
    big_premis_t=[]
    for s in range(len(big)):
        half_k=(big[s][0][1]-big[s][0][0])//2
#####################################kye#############################################################
        if half_k>=3 :#####Important parameters that can be adjusted appropriately, usually between 3 and 9
            half_k=2#####between 1 and 3
        for w in range(half_k):
            if big[s][1]+w<len(d2_data) and big[s][1]-w>0:
                if d2_data[big[s][1]+w]>=0 or d2_data[big[s][1]-w]>=0:
                    big_premis.append(s)
    big_premis=list(set(big_premis))
    for s in big_premis:
        big_premis_t.append(big[s])
    print(big_premis_t)
    for s in  big_premis_t:
        big.remove(s)
    for m in range(len(big)-1):
        if data[big[m][0][1]]>data[big[m][0][0]]:
            if data[big[m][0][1]]-data[big[m][0][0]]>0:
                list1=[]
                for f in range(big[m][1],big[m][0][1]):
                    list1.append(abs(data[f]-data[big[m][0][1]]))
                big[m][0][1]=list1.index(min(list1))+big[m][1]
                del list1
        else:
                if data[big[m][0][0]]-data[big[m][0][1]]>0:
                    list1=[]
                    for f in range(big[m][0][0],big[m][1]):
                        list1.append(abs(data[f]-data[big[m][0][1]]))
                    big[m][0][0]=list1.index(min(list1))+big[m][0][0]
                    del list1
    print('----------------')
    m=5#m-parameter, adjust the width of the reserved peak (inverse ratio)
    for y in range(len(big)-1):
        q=big[y][0][1]-big[y][0][0]
        rush=q//2-int(q//m)
        data_temp1=data[big[y][0][0]+rush:big[y][1]+1]
        data_temp2=data[big[y][1]:big[y][0][1]+1-rush]
        flag1=0
        flag2=0
        for h in range(len(data_temp1)-1):
            if data_temp1[h+1]-data_temp1[h]<0:
                flag1=flag1+1
        for x in range(len(data_temp2)-1):
            if data_temp2[x+1]-data_temp2[x]>0:
                flag2=flag2+1
#        if q<5 :
#            big_mis.append(big[y])
#    for s in big_mis:
#        if s in big:
#            big.remove(s)
    print(big)
    big_new=[]
    small_new=[]
    for b in range(len(big)):
        small_new.append(big[b][0][0])
        small_new.append(big[b][0][1])
    for u in range(len(big)):
        big_new.append(big[u][1])
    for r in range(0,len(small_new)-1,2):
        q=small_new[r+1]-small_new[r]
        for t in range(1,int(q//m)+1):
            big_new.append(big_new[r//2]+t)
            big_new.append(big_new[r//2]-t)
    big_new.sort()
    #print(big_new)
    big_new_searching=[]
    for i in big_new:
        if i > len(data)-2 or i <1:
            big_new_searching.append(i)
    for i in big_new_searching:
        big_new.remove(i)
    return big_new,data_temp

        
def weight_resultX2(data):#PEER
    d_data,d2_data=derivative(data)
    big_new,data_temp=find_extreme(data,d_data,d2_data)
    new_data=weight_result(data_temp,11)#window size
    for l in big_new:
        new_data[l]=data[l]
    return new_data


def read(filename):
    file = open(filename,encoding='utf-8')
    data_lines = file.readlines()
    file.close
    orign_keys = []
    orign_values = []
    for data_line in data_lines:
        pair = data_line.split()
        key = float(pair[0])
        value = float(pair[1])
        orign_keys.append(key)
        orign_values.append(value)
    return orign_keys, orign_values
	
	
def write(filename, keys, values):
    file = open(filename, 'w')
    for k, v in zip(keys, values):
        file.write(str(k) + " " + str(v) + "\n")
    file.close()


def main(top_dir):
         time_start = time.time() #time
         files=os.listdir(top_dir)
         files.sort()
         for i in range(len(files)):
             file=files[i]
             file=os.path.join(top_dir,file)
             file=file.replace('\\','/')
             key,values=read(file)
             smooth_data1=weight_resultX2(values)
             root, ext = os.path.splitext(os.path.basename(file))
             head, tail = os.path.split(file)
             c=os.path.join(head+'/denoised')
             isExists=os.path.exists(c)
             if not isExists:
                 os.makedirs(c) 
             #write(os.path.join(c,root + 'raw.txt'), key, values)
             write(os.path.join(c,root + 'byPEER1.txt'), key, smooth_data1)
             time_end = time.time() 
             time_c= time_end - time_start#time up
             print(time_c)


                           
#————————test————————#
if __name__ == "__main__":
    main('C:/Users/lgkgroup/Desktop/test')#Drop the total folder path here
