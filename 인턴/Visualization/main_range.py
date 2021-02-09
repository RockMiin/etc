#!/usr/local/bin/python3.7

import dpkt
import ipaddress
from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
# harvard.edu
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test.pcap"
# filename= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\Debug_test_2.pcap"
# filename= "G:\내 드라이브\인턴(20.12.23- 21.02.15)\Tor Packet\data\Debug192.168.1.10-1.pcap"
# file_dir= "C:\\Users\\aideep\\Desktop\\Tor-WinApp_1116 (1)\\Tor_WinApp\\bin\\python_pcap\\"
file_dir="G:\\내 드라이브\\인턴(20.12.23- 21.02.15)\\Tor Packet\\all_packet\\"
file_list= os.listdir(file_dir)
# print(file_list)
ip_range= '192.168.1.10'

def load_data(file_dir, filename, x_idx):
    global acc
    global x_threshold
    global tmp
    global tmp_min_idx
    global tmp_max_idx
    filename = file_dir + filename

    time = []
    div_time = [0]
    size = []

    idx = 0
    for ts, pkt in dpkt.pcap.Reader(open(filename, 'rb')):
        if idx == 0: tmp_time = ts

        eth = dpkt.ethernet.Ethernet(pkt)
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            continue
        idx += 1
        ip = eth.data
        time.append(round(ts - tmp_time, 4))
        size.append(len(pkt))

    for i in range(1, len(time)):
        div_time.append(abs(round(time[i] - time[i - 1], 4)))

    df= pd.DataFrame({'time': div_time, 'size': size})
    time_max_idx= df['time'].idxmax()

    # tmp에서 threshold를 넘는 최초의 값의 index를 저장
    tmp = 0
    for i, item in enumerate(df['time']):
        if item > x_threshold[x_idx]:
            tmp= i; break;

    tmp_max_idx= 0
    tmp_min_idx= 0

    sum_time = 0
    for i in range(tmp + 1, len(df['time'])):
        sum_time += df['time'][i]
        # print(filename ,tmp, i, df['time'][i], sum_time)
        if sum_time > time_interval:
            tmp_max_idx= i
            # print("sum_time: ", sum_time)
            break;

    sum_time = 0
    for i in range(tmp-1, 0, -1):
        sum_time+= df['time'][i]
        # print(filename, tmp, i, df['time'][i], sum_time)
        if sum_time > time_interval:
            tmp_min_idx = i
            # print("sum_time: ", sum_time)
            break;

    # print(tmp)
    if tmp_min_idx<= time_max_idx<= tmp_max_idx:
        acc[x_idx]+=1;

    print('min :', tmp_min_idx, 'max :', tmp_max_idx, "tmp :", tmp, "max_idx: ", time_max_idx)
    return df

def MA_filter(df):
    df['time']= df['time'].rolling(100, min_periods=1).mean()
    df['size']= df['size'].rolling(100, min_periods=1).mean()

    return df

def std_scaler(data):
    std_data= (data- min(data))/(max(data)-min(data))
    return std_data

def plot_data(df):
    global filename
    global tmp
    global tmp_min_idx
    global tmp_max_idx
    x = np.linspace(0, df['time'].shape[0], df['time'].shape[0])
    plt.subplot(2, 1, 1)
    # peaks, _ = find_peaks(df['time'], distance=500)
    plt.plot(x, df['time'])
    # plt.scatter(tmp, df['time'][tmp_min_idx], s= 100, c='green')
    # plt.scatter(tmp, df['time'][tmp_max_idx], s= 50, c='yellow')
    plt.axline((0, 0), (0,df['time'][tmp_min_idx]), color= 'g', linestyle= '--')
    # plt.axvline(x= tmp_min_idx, color= 'r', linestyle= '--')
    plt.scatter(tmp, df['time'][tmp], s= 100, c='blue')
    # plt.scatter(int(df['time'].idxmax()*0.8), df['time'][int(df['time'].idxmax()*0.8)], s= 50, c='blue')
    plt.scatter(df['time'].idxmax(), df['time'][df['time'].idxmax()], s= 50, c='red')


    plt.subplot(2, 1, 2)
    x = np.linspace(0, df['size'].shape[0], df['size'].shape[0])
    plt.xlabel(filename)
    plt.plot(x, df['size'])
    plt.show()

# load entrynode
# EntryNode= []
# with open("G:\내 드라이브\인턴(20.12.23- 21.02.15)\Tor Packet\EntryNode.txt", 'r') as file:
#     for text in file:
#         EntryNode.append(text.strip('\n'))
#
max_time= []
mean_threshold = 5.6 # 미리 측정
mean_val= 0.012
std_val= 0.0497
time_interval= 0.1
x_threshold = np.round(np.linspace(mean_threshold - 4, mean_threshold+1, 50), 3)
acc = [0] * len(x_threshold)
for idx, value in enumerate(x_threshold):
    x_threshold[idx]= x_threshold[idx]-(mean_val+ 6*std_val)
    print(idx, value, x_threshold[idx], (mean_val+ 6*std_val))

    for filename in file_list:
        df = load_data(file_dir, filename, idx)
        df['time']= df['time'].fillna(method='bfill')
        # df= MA_filter(df)
        # print(df['time'])
        # print(df['time'].max())
        # print(df['time'].idxmax())
        max_time.append(df['time'].max())
        # print(df['time'].isnull().sum())

        plot_data(df)

    # print(max_time)

    print(acc)

for i in range(len(acc)):
    acc[i] = round((acc[i] / (len(file_list))) * 100, 1)
plt.ylabel("accuracy")
plt.xlabel("threshold")

plt.plot(x_threshold, acc)
plt.show()

# calculate std, mean graph
# idx= 0
# normal_mean= []
# normal_std= []
# for filename in file_list:
#     df = load_data(file_dir, filename, idx)
#     df['time'].fillna(method='bfill')
#     # print(df['time'])
#     # df= MA_filter(df
#     # print(df['time'].max())
#     # print(df['time'].idxmax())
#     # print(int(df['time'].idxmax()*0.8))
#     avg= df['time'].iloc[:int(df['time'].idxmax()*0.8)].mean()
#     std= df['time'].iloc[:int(df['time'].idxmax()*0.8)].std()
#     normal_mean.append(avg)
#     normal_std.append(std)
#     max_time.append(df['time'].max())
#     # print(df['time'].isnull().sum())
#     # print(filename, avg, std)
#     plot_data(df)
# mean_val= round((sum(normal_mean)/len(normal_mean)), 4)
# std_val= round((sum(normal_std)/len(normal_std)), 4)
# print("mean val:", mean_val, "std_val", std_val)
