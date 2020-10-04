from random import randrange, randint, seed
from traffic_generator import TrafficGenerator
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import csv
seed(314)

def get_digits(n):

    digits=0
    while(n>0):
        digits+=1
        n=n//10
        
    return digits

NUMBER_OF_COS = 3
TRAFFIC_FILE = "GEANT_AMS-FRA_24h_traffic.csv"
SECONDS_OF_TRAFFIC = 300
INTERFACE_SPEED = 1*10**9  # 1Gbps
PERCENTAGE = 1
SLOTS = int((INTERFACE_SPEED/(4500*8))*(PERCENTAGE/100))
SLOTS_OOM = get_digits(SLOTS)

COS0 = 60
COS1 = 30
COS2 = 10

def main():

    # *** INITIALIZATION PHASE ***
    ## set constant variables
    traffic_distribution_per_cos = [COS0, COS1, COS2]

    ## import data & preprocessing
    geant_traffic_data = import_csv(TRAFFIC_FILE)
    throughput = preprocess_data(geant_traffic_data)

    ## setup a traffic generator
    tg = TrafficGenerator(throughput, traffic_distribution_per_cos)
     
    ## initialize variables for plots
    estimated_tot_throughput = np.array([])
    estimated_cos0_percent = np.array([])
    estimated_cos1_percent = np.array([])
    estimated_cos2_percent = np.array([])

    # *** EXECUTION PHASE ***
    x=1
    for t in range(len(throughput)):
        
        traffic_t = tg.traffic[t]
        
        oom_t = morris_algo(traffic_t)
        sample_t = vitter_algo(traffic_t, SLOTS)

        estimated_throughput_t = estimate_throughput(sample_t, oom_t)

        #! TROUBLESHOOTING PURPOSE
        #print("{} --> ESTIMATED = {}K || REAL = {}K || OOM RATIO (real/est) = {} || SAMPLING RATIO (slots/real) {} || COS DISTRO {}".format(t,estimated_throughput_t[0]//10**3, throughput[t]//10**3, 
        #get_digits(len(traffic_t))/oom_t, SLOTS/len(traffic_t), "{}|{}|{}".format(int(100*estimated_throughput_t[1]/estimated_throughput_t[0]),int(100*estimated_throughput_t[2]/estimated_throughput_t[0]),int(100*estimated_throughput_t[3]/estimated_throughput_t[0]))))

        # SAVE DATA FOR PLOTS
        estimated_tot_throughput = np.append(estimated_tot_throughput, estimated_throughput_t[0])
        estimated_cos0_percent = np.append(estimated_cos0_percent, 100*(estimated_throughput_t[1]/estimated_throughput_t[0]))
        estimated_cos1_percent = np.append(estimated_cos1_percent, 100*(estimated_throughput_t[2]/estimated_throughput_t[0]))
        estimated_cos2_percent = np.append(estimated_cos2_percent, 100*(estimated_throughput_t[3]/estimated_throughput_t[0]))
        
        # PROGRESS BAR
        if t == (x*int(len(throughput)/100)):
            print("PROGRESS IS @ {}%: {}".format(x, x*'='+'>'))
            x+=1

    # *** PLOT RESULTS PHASE ***
    ## THROUGHPUT
    fig = plt.figure(1,figsize=(10,10))
    fig.suptitle('Big Data Network Analyzer (BDNA)', fontsize=16)
    plt.xlabel('Time [s]')
    plt.ylabel('Throughput [bit/s]')
    plt.title('Total Throughput Estimation - MEMORY = {}% OF INTERFACE CAPACITY'.format(PERCENTAGE))

    xdata = np.arange(SECONDS_OF_TRAFFIC)  
    plt.plot(xdata, estimated_tot_throughput, 'rx')
    plt.plot(xdata,throughput, 'b--', linewidth=2)
    
    plt.show()

    ## COS DISTRIBUTION
    fig = plt.figure(2,figsize=(10,10))
    fig.suptitle('Big Data Network Analyzer (BDNA)', fontsize=16)
    plt.xlabel('Time [s]')
    plt.ylabel('COS PERCENTAGE [%]')
    plt.title('CoS Distribution Estimation - MEMORY = {}% OF INTERFACE CAPACITY'.format(PERCENTAGE))

    xdata = np.arange(SECONDS_OF_TRAFFIC)  
    # COS0
    plt.plot(xdata, estimated_cos0_percent, 'bx')
    real_cos0_percent = np.array(SECONDS_OF_TRAFFIC * [COS0])
    plt.plot(xdata, real_cos0_percent, 'r--', linewidth=2)
    # COS1
    plt.plot(xdata, estimated_cos1_percent, 'yx')
    real_cos1_percent = np.array(SECONDS_OF_TRAFFIC * [COS1])
    plt.plot(xdata, real_cos1_percent, 'r--', linewidth=2)
    # COS2
    plt.plot(xdata, estimated_cos2_percent, 'gx')
    real_cos2_percent = np.array(SECONDS_OF_TRAFFIC * [COS2])
    plt.plot(xdata, real_cos2_percent, 'r--', linewidth=2)

    plt.show()


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
    scale_factor = (300*10**9)/INTERFACE_SPEED  #! traffic data was taken from a 300Gbps interface
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
    t0 = randrange(seconds_in_day - SECONDS_OF_TRAFFIC)
    t1 = t0+SECONDS_OF_TRAFFIC

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

def estimate_throughput(sample, oom):

    scale_factor = 10**(oom-SLOTS_OOM)

    # *** ESTIMATE VOLUME ***
    sample_volume = 0
    for frame in sample:
        sample_volume+=frame[1]
    
    estimated_volume = sample_volume*scale_factor
    
    # *** ESTIMATE DISTRIBUTION ***
    estimated_distribution = []

    volume_cos = []
    for i in range(NUMBER_OF_COS):
        volume_cos.append(0)
    
    for frame in sample:
        j = frame[0]
        volume_cos[j]+=frame[1]
    
    for i in range(NUMBER_OF_COS):
        estimated_distribution.append((volume_cos[i]/estimated_volume)*scale_factor)
    
    # *** CALCULATE THROUGHPUT AND RETURN RESULTS ***
    estimated_throughput = []
    
    estimated_throughput_tot = estimated_volume*8
    estimated_throughput.append(estimated_throughput_tot)

    for i in range(NUMBER_OF_COS):
        estimated_throughput.append(int(estimated_distribution[i]*estimated_throughput_tot))
    
    return estimated_throughput


    sum = 0
    for i in range(order):
        sum += sequence[-(i+1)]
    sequence[-1] = sum/order

    return sequence


if __name__ == "__main__":
    main()