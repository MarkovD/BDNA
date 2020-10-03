from random import randrange, randint, seed
from traffic_generator import TrafficGenerator
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time
import csv
seed()

TRAFFIC_FILE = "GEANT_AMS-FRA_24h_traffic.csv"

def main():

    #*** INITIALIZATION PHASE ***
    ## set constant variables
    traffic_distribution_per_cos = [[20, 1000], [30, 4000], [50, 6000]]

    ## import data & preprocessing
    geant_traffic_data = import_csv(TRAFFIC_FILE)
    throughput = preprocess_data(geant_traffic_data)

    ## setup a traffic generator
    tg = TrafficGenerator(throughput, traffic_distribution_per_cos)

    start_time = time.time()
    for t in range(len(throughput)):
        tg.traffic[s]
    print("--- %s seconds ---" % (time.time() - start_time))

def initiali():
    pass

def morris_algo(sequence):
    
    order_of_magnitude = 0

    i=0
    while i < len(sequence):
        
        random_int = randrange(10**order_of_magnitude)
        
        if random_int == 0:
            order_of_magnitude += 1
        
        i+=1

    return order_of_magnitude

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
    seconds_in_day = 60*60*24

    # Remove Header
    data.pop(0)

    # Extract throughput values
    geant_throughput = []
    real_time = np.linspace(0,seconds_in_day,len(data))
    
    for i in range(len(data)):
        geant_throughput.append(float(data[i][1]))

    ## INTERPOLATE DATA
    # from 1 sample every 5 minutes to 1 sample per second
    interp_cubic = interp1d(real_time, geant_throughput, kind='cubic')
    interp_time = np.linspace(0, seconds_in_day, seconds_in_day)
    interp_throughput = interp_cubic(interp_time)
    
    #plt.plot(real_time,geant_throughput, 'o')
    #plt.plot(interp_time,interp_throughput, '--')
    #plt.show()

    return [int(i) for i in interp_throughput]
    

if __name__ == "__main__":
    main()