from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import serial
import BlynkLib
from time import sleep

blynk=BlynkLib.Blynk('H2ajExldKt1umhBDhToljgeQePp_ojem')
ser1=serial.Serial('COM3',9600)
ser=serial.Serial('COM5',9600,timeout=1);

def get_serial1_data():
    pre=[]
    d=[]
    count=0
    while count<=3:
        sleep(0.1)
        data=ser.readline().decode('utf-8',errors='replace')
        sp=data.split(':')
        print(sp)
        v=sp[1].split('\r')[0]
        if(sp[0]=='ir1'):
            pre.append(v)
            blynk.virtual_write(10,v)
            count+=1
        if(sp[0]=='ir2'):
            pre.append(v)
            blynk.virtual_write(11,v)
            count+=1
        
        if(sp[0]=='ir3'):
            pre.append(v)
            blynk.virtual_write(12,v)
            count+=1
    d.append(pre)
    print('number of itteration: {} list value: {}'.format(count,d))
    return predict_road1_status(d)
    d=[]
    
def predict_road1_status(pre):
    out=['1']
    dataset=pd.read_csv('test.csv')
    dataset.set_index('ir1',drop=False)
    x=dataset.loc[0:101,'ir1':'ir4']
    y=dataset.loc[0:100,'traffic']
    knn=KNeighborsClassifier(n_neighbors=3)
    knn.fit(x,y)
    out=knn.predict(pre)
    print(out[0])
    return out[0]
    #print(accuracy_score(y,out))

def get_serial2_data():
    sleep(0.1)
    pre=[]
    d=[]
    count=0
    while count<=3:
        
        data=ser1.readline().decode('utf-8',errors='replace')
        sp=data.split(':')
        v=sp[1].split('\r')[0]
        print(sp)
        if(sp[0]=='ir1'):
            pre.append(v)
            blynk.virtual_write(13,v)
            count+=1
        if(sp[0]=='ir2'):
            pre.append(v)
            blynk.virtual_write(14,v)
            count+=1
        
        if(sp[0]=='ir3'):
            pre.append(v)
            blynk.virtual_write(15,v)
            count+=1
    d.append(pre)
    print('number of itteration: {} list value: {}'.format(count,d))
    return predict_road2_status(d)
    d=[]
    
def predict_road2_status(pre):
    out=['1']
    dataset=pd.read_csv('test.csv')
    dataset.set_index('ir1',drop=False)
    x=dataset.loc[0:101,'ir1':'ir4']
    y=dataset.loc[0:100,'traffic']
    knn=KNeighborsClassifier(n_neighbors=3)
    knn.fit(x,y)
    out=knn.predict(pre)
    print(out[0])
    return out[0]
    #print(accuracy_score(y,out))

def comp():
    d1=get_serial1_data()
    d2=get_serial2_data()
    print("road1 congestion: {} \nRoad2 Congestion: {}".format(d1,d2))
    if(d1<d2):
        print("Lane1 has less traffic")
        blynk.virtual_write(16,"lane1 clear")
    if(d1>d2):
        print("Lane2 has less traffic")
        blynk.virtual_write(16,"lane2 clear")
    if(d1==d2):
        print("Equal")
        blynk.virtual_write(16,"Equal")
    
while True:
    blynk.run()
    comp()
    sleep(0.1)
#extract_data()
