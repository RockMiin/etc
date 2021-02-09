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
# file_dir='./all_packet\\'
file_list= os.listdir(file_dir)
# print(file_list)
ip_range= '192.168.1.10'


def load_data(file_dir, filename):

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

    df = pd.DataFrame({'time': div_time, 'size': size})

    return df

def load_data_threshold_cnt(file_dir, filename, x_idx):
    global acc
    global x_threshold
    global tmp
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

    tmp = 0
    for i, item in enumerate(df['time']):
        if item > x_threshold[x_idx]:
            tmp= i; break;
    # print(tmp)
    if df['time'].idxmax()-100< tmp < df['time'].idxmax()+100:
        acc[x_idx]+=1;

    return df

def MA_filter(df):
    df['time']= df['time'].rolling(100).mean()
    df['size']= df['size'].rolling(100).mean()

    return df

def std_scaler(data):
    std_data= (data- min(data))/(max(data)-min(data))
    return std_data

def plot_data(df):
    global filename
    global tmp
    x = np.linspace(0, df['time'].shape[0], df['time'].shape[0])
    plt.subplot(2, 1, 1)
    plt.plot(x, df['time'])

    # plt.scatter(tmp, df['time'][tmp], s= 100, c='blue')
    # plt.scatter(int(df['time'].idxmax()*0.8), df['time'][int(df['time'].idxmax()*0.8)], s= 50, c='blue')
    # plt.scatter(df['time'].idxmax(), df['time'][df['time'].idxmax()], s= 50, c='red')


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

def calculate_normal():

    idx= 0
    normal_mean= []
    normal_std= []
    for filename in file_list:
        df = load_data_threshold_cnt(file_dir, filename, idx)
        df['time'].fillna(method='bfill')
        # print(df['time'])
        # df= MA_filter(df
        # print(df['time'].max())
        # print(df['time'].idxmax())
        # print(int(df['time'].idxmax()*0.8))
        avg= df['time'].iloc[:int(df['time'].idxmax()*0.8)].mean()
        std= df['time'].iloc[:int(df['time'].idxmax()*0.8)].std()
        normal_mean.append(avg)
        normal_std.append(std)
        max_time.append(df['time'].max())
        # print(df['time'].isnull().sum())
        # print(filename, avg, std)
        plot_data(df)
    mean_val= round((sum(normal_mean)/len(normal_mean)), 4)
    std_val= round((sum(normal_std)/len(normal_std)), 4)
    print("mean val:", mean_val, "std_val", std_val)
    return mean_val, std_val

def threshold_range(max_time, mean_threshold, mean_val, std_val, x_threshold, acc):

    for idx, value in enumerate(x_threshold):
        print(idx, value)
        x_threshold[idx]= x_threshold[idx]-(mean_val+ 6*std_val)
        print(x_threshold[idx], value,(mean_val+ 6*std_val) )
        for filename in file_list:
            df = load_data(file_dir, filename, idx)
            df['time'].fillna(method='bfill')
            # print(df['time'])
            # df= MA_filter(df)
            # print(df['time'].max())
            # print(df['time'].idxmax())
            max_time.append(df['time'].max())
            # print(df['time'].isnull().sum())

            # plot_data(df)

        # print(max_time)
    mean_threshold = round(sum(max_time) / len(max_time), 1)
    print("mean :", mean_threshold)
    print(acc)

    for i in range(len(acc)):
        acc[i] = round((acc[i] / (len(file_list))) * 100, 1)
    plt.ylabel("accuracy")
    plt.xlabel("threshold")

    plt.plot(x_threshold, acc)
    plt.show()

max_time= []
mean_threshold = 5.6 # 미리 측정
mean_val= 0.012
std_val= 0.0497
x_threshold = np.round(np.linspace(mean_threshold - 5, mean_threshold+1, 50), 3)
acc = [0] * len(x_threshold)

for filename in file_list:
    df = load_data(file_dir, filename)
    df['time'].fillna(method='bfill')
    # print(df['time'])
    # df= MA_filter(df
    # print(df['time'].max())
    # print(df['time'].idxmax())
    max_time.append(df['time'].max())
    # print(df['time'].isnull().sum())

    plot_data(df)
print(df)

# print(max_time)
mean_threshold = round(sum(max_time) / len(max_time), 1)
print("mean :", mean_threshold)
print(acc)
mean_val, std_val= calculate_normal()
# threshold_range(max_time, mean_threshold, mean_val, std_val, x_threshold, acc)

