from random import randrange, randint, seed
from traffic_generator import TrafficGenerator
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('TkAgg')
#import pandas as pd
import time
import csv
seed()

TRAFFIC_FILE = "GEANT_AMS-FRA_24h_traffic.csv"
SLOTS = 100
NUMBER_OF_COS = 3

def main():

    #*** INITIALIZATION PHASE ***
    ## set constant variables
    traffic_distribution_per_cos = [[20, 6000], [30, 2000], [50, 800]]

    ## import data & preprocessing
    geant_traffic_data = import_csv(TRAFFIC_FILE)
    throughput = preprocess_data(geant_traffic_data)

    ## setup a traffic generator
    tg = TrafficGenerator(throughput, traffic_distribution_per_cos)

    ## SETUP GRAPH

    fig = plt.figure(figsize=(10,10))
    plt.xlabel('seconds')
    plt.ylabel('throughput [bit/s]')
    plt.title('BIGDATA-SHARK')

    xdata = np.arange(3600)    

    estimated_tot_throughput = np.array([])
    estimated_cos0_throughput = np.array([])
    estimated_cos1_throughput = np.array([])
    estimated_cos2_throughput = np.array([])

    for t in range(len(throughput)):
        
        traffic_t = tg.traffic[t]
        
        oom_t = morris_algo(traffic_t)
        sample_t = vitter_algo(traffic_t, SLOTS)

        estimated_throughput_t = estimate_throughput(sample_t, oom_t)

        estimated_tot_throughput = np.append(estimated_tot_throughput, estimated_throughput_t[0])
        estimated_cos0_throughput = np.append(estimated_cos0_throughput, estimated_throughput_t[1])
        estimated_cos1_throughput = np.append(estimated_cos1_throughput, estimated_throughput_t[2])
        estimated_cos2_throughput = np.append(estimated_cos2_throughput, estimated_throughput_t[3])
    
    plt.plot(xdata,throughput, 'o')
    plt.plot(xdata, estimated_tot_throughput, 'x')
    plt.plot(xdata, estimated_cos0_throughput, '-')
    plt.plot(xdata, estimated_cos0_throughput+estimated_cos1_throughput, '-')
    plt.plot(xdata, estimated_cos0_throughput+estimated_cos1_throughput+estimated_cos2_throughput, '-')
    plt.show()
    print("FINE")


def import_csv(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if row:  # avoid blank lines
                data.append(row)
    return data

def preprocess_data(data):

    # init constant variables
    scale_factor = 300  # data was taken from a 300Gbps interface
    seconds_in_day = 60*60*24

    # Remove Header
    data.pop(0)

    # Extract throughput values
    geant_throughput = []
    real_time = np.linspace(0,seconds_in_day,len(data))
    
    for i in range(len(data)):
        geant_throughput.append(float(data[i][1])/scale_factor)

    ## INTERPOLATE DATA
    # from 1 sample every 5 minutes to 1 sample per second
    interp_cubic = interp1d(real_time, geant_throughput, kind='cubic')
    interp_time = np.linspace(0, seconds_in_day, seconds_in_day)
    interp_throughput = interp_cubic(interp_time)
    
    #plt.plot(real_time,geant_throughput, 'o')
    #plt.plot(interp_time,interp_throughput, '--')
    #plt.show()

    # Randomly extract 1hour of traffic out of the whole day
    t0 = randrange(seconds_in_day - 3600)
    t1 = t0+3600

    return [int(interp_throughput[i]) for i in range(t0, t1)]

def morris_algo(sequence):
    
    order_of_magnitude = 0

    i=0
    while i < len(sequence):
        
        random_int = randrange(10**order_of_magnitude)
        
        if random_int == 0:
            order_of_magnitude += 1
        
        i+=1

    return order_of_magnitude

def vitter_algo(stream, slots):
    
    sampled_stream = []

    sampled_stream = stream[0:slots]

    for i in range(slots, len(stream)):
        j = randrange(1,i)
        if j <= slots:
            sampled_stream[j-1] = stream[i]

    return sampled_stream

def estimate_volume(sample, oom):
    
    sample_volume = 0
    for frame in sample:
        sample_volume+=frame[1]
    
    estimated_volume = sample_volume*(10**(oom-2))
    return estimated_volume

def estimate_distribution(sample, estimated_volume, NUMBER_OF_COS):

    estimated_distribution = []

    volume_cos = []
    for i in range(NUMBER_OF_COS):
        volume_cos.append([i,0])
    
    for frame in sample:
        j = frame[i]
        volume_cos[j][1]+=frame[1]
    
    for i in range(NUMBER_OF_COS):
        estimated_distribution.append([i,int(volume_cos[i][1]/estimated_volume)])
    
    return estimated_distribution

def estimate_throughput(sample, oom):

    scale_factor = 10**(oom-2)

    ## ESTIMATE VOLUME
    sample_volume = 0
    for frame in sample:
        sample_volume+=frame[1]
    
    estimated_volume = sample_volume*scale_factor
    
    ## ESTIMATE DISTRIBUTION
    estimated_distribution = []

    volume_cos = []
    for i in range(NUMBER_OF_COS):
        volume_cos.append(0)
    
    for frame in sample:
        j = frame[0]
        volume_cos[j]+=frame[1]
    
    for i in range(NUMBER_OF_COS):
        estimated_distribution.append((volume_cos[i]/estimated_volume)*scale_factor)
    
    ## CALCULATE THROUGHPUT AND RETURN RESULTS
    estimated_throughput = []
    
    estimated_throughput_tot = estimated_volume*8
    estimated_throughput.append(estimated_throughput_tot)

    for i in range(NUMBER_OF_COS):
        estimated_throughput.append(int(estimated_distribution[i]*estimated_throughput_tot))
    
    return estimated_throughput


if __name__ == "__main__":
    main()