#!/usr/local/bin/python3.7

import dpkt
import ipaddress
from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ignore:RuntimeWarning
# harvard.edu
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test.pcap"
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test_2.pcap"
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\python_pcap\\Debug192.168.1.10-3.pcap"
# file_dir= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\python_pcap\\"
# file_dir= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\apache.org\\"
file_dir="G:\\내 드라이브\\인턴(20.12.23- 21.02.15)\\Tor\\Tor_WinApp\\bin\\archive.org\\"

file_list= os.listdir(file_dir)
print(file_list)
ip_range= '192.168.1.10'

EntryNode= []
res= []
time= []
packet= []
div_time= [0]
size= []
idx= []

# with open('G:\내 드라이브\Tor Packet\EntryNode.txt', 'r') as file:
#     for text in file:
#         EntryNode.append(text.strip('\n'))
idx= 0
print("packet append")

avg_time= []
dev_time= []

pkg_time= []
thres_point= []


for filename in file_list:
    filename= file_dir + filename

    res = []
    time = []
    packet = []
    div_time = [0]
    size = []

    for ts, pkt in dpkt.pcap.Reader(open(filename,'rb')):
        if idx==0: tmp_time= ts

        eth=dpkt.ethernet.Ethernet(pkt)
        if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
           continue

        ip=eth.data
        idx+=1
        time.append(round(ts-tmp_time, 4))
        size.append(len(pkt))

    for i in range(1, len(time)):
        div_time.append(abs(round(time[i]-time[i-1], 4)))

    df = pd.DataFrame({'time': div_time, 'size': size})

    # def std_scaler(data):
    #     std_data = (data - min(data)) / (max(data) - min(data))
    #     return std_data
    #
    # df['time']= std_scaler(df['time'])
    # df['size']= std_scaler(df['size'])

    avg= df['time'].iloc[:int(df['time'].shape[0]*0.8)].mean()
    std= df['time'].iloc[:int(df['time'].shape[0]*0.8)].std()
    # print(avg, std)
    threshold= avg+8*std
    print("thres:", threshold)

    flag= False
    start, end= 0, 0
    for idx, value in enumerate (df['time'].iloc[int(df['time'].shape[0]*0.8):]):
        if value > threshold and flag== False:
            start= int(df['time'].shape[0]*0.8)+idx; flag= True
        if value< threshold and flag== True:
            end= int(df['time'].shape[0]*0.8)+idx
    thres_point.append([start, end])
    print(start, end)
    pkg_time.append([round(df['time'].iloc[start:end].mean(),4), round(df['time'].iloc[start:end].min(),4)
                        ,round(df['time'].iloc[start:end].max(), 4)])

    plt.subplot(2, 1, 1)

    x = np.linspace(0, df['time'].shape[0], df['time'].shape[0])
    plt.plot(x, df['time'])
    plt.scatter(start, df['time'].iloc[start], c= 'red', s=10)
    plt.scatter(end, df['time'].iloc[end], c= 'red', s=10)

    # x = np.linspace(0, df['time'].shape[0], df['time'].shape[0])
    # plt.subplot(2, 1, 1)
    # plt.plot(x, df['time'])
    #
    plt.subplot(2, 1, 2)
    x = np.linspace(0, df['size'].shape[0], df['size'].shape[0])
    plt.plot(x, df['size'])
    plt.show()

# for i in pkg_time:
#     print(i)





