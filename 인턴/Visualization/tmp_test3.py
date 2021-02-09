#!/usr/local/bin/python3.7

import dpkt
import ipaddress
from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np

# harvard.edu
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test.pcap"
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test_2.pcap"
filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\python_pcap\\Debug192.168.1.10-2.pcap"
# file_dir= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\python_pcap\\"
# file_list= os.listdir(file_dir)
# print(file_list)
ip_range= '192.168.1.10'

EntryNode= []
res= []
time= []
packet= []
div_time= [0]
size= []
idx= []

with open("G:\내 드라이브\인턴(20.12.23- 21.02.15)\Tor Packet\EntryNode.txt", 'r') as file:
    for text in file:
        EntryNode.append(text.strip('\n'))
idx= 0
print("packet append")

# for filename in file_list:
#     filename= file_dir + filename
#     for ts, pkt in dpkt.pcap.Reader(open(filename,'rb')):
#         if idx==0: tmp_time= ts
#
#         eth=dpkt.ethernet.Ethernet(pkt)
#         if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
#            continue
#
#         ip=eth.data
#         idx+=1
#         time.append(round(ts-tmp_time, 4))
#         size.append(len(pkt))
#
#     # print(round(ts-tmp_time, 4))
#     for i in range(1, len(time)):
#         div_time.append(abs(round(time[i]-time[i-1], 4)))
#
#     # print(div_time)
#     # print(div_time)
#     # print(len(div_time), len(size))
#     # print(size)
#
#     x= np.linspace(0, len(div_time), len(div_time))
#     plt.subplot(2, 1, 1)
#     plt.plot(x, div_time)
#     # plt.xlabel("time")
#
#     plt.subplot(2, 1, 2)
#     x= np.linspace(0, len(size), len(size))
#     # print(x.shape, len(size))
#     # plt.xlabel('size')
#     plt.plot(x, size)
#     plt.show()

idx= 0
for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
    if idx == 0: tmp_time = ts

    eth = dpkt.ethernet.Ethernet(pkt)
    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
        continue
    idx+=1
    ip = eth.data
    time.append(round(ts - tmp_time, 4))
    size.append(len(pkt))

# print(round(ts-tmp_time, 4))
for i in range(1, len(time)):
    div_time.append(abs(round(time[i] - time[i - 1], 4)))

import pandas as pd
import csv

# f= open('size.txt', 'w')
# for i in range(len(div_time)):
#     f.write(str(size[i])+'\n')
# f.close()

# x = np.linspace(0, len(div_time), len(div_time))
# plt.subplot(2, 1, 1)
# plt.plot(x, div_time)
# # plt.xlabel("time")
#
# plt.subplot(2, 1, 2)
# x = np.linspace(0, len(size), len(size))
# # print(x.shape, len(size))
# # plt.xlabel('size')
# plt.plot(x, size)
# plt.show()

import plotly.graph_objects as go
import pandas as pd
from scipy.signal import find_peaks

df= pd.DataFrame({'time': div_time, 'size': size})
print(df['time'].shape, df['size'].shape)
df['time']= df['time'].rolling(500).mean()
df['size']= df['size'].rolling(500).mean()
print(df['time'].shape, df['size'].shape)

df['time'].fillna(method='ffill')


x= np.linspace(0, df['time'].shape[0], df['time'].shape[0])
plt.subplot(2, 1, 1)
peaks, _ = find_peaks(df['time'], distance=500)
print(df['time'])
# print(peaks)
# plt.plot(peaks, x[peaks], "x")
plt.plot(x, df['time'])


# plt.plot(np.zeros_like(x), "--", color="gray")

plt.subplot(2, 1, 2)
x= np.linspace(0, df['size'].shape[0], df['size'].shape[0])
plt.plot(x, df['size'])
plt.show()










