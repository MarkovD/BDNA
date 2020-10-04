from random import shuffle, gauss,seed
seed(314)

class TrafficGenerator():
    
    def __init__(self, throughput, traffic_cos_data):
        
        self.throughput = throughput  #bit/s
        self.volume = [int(t/8) for t in self.throughput]   #bytes/s

        self.traffic_cos_data = traffic_cos_data

        self.traffic = []

        x = 1
        for t in range(len(self.volume)):
            
            traffic_t = []
            #
            for n in range(len(traffic_cos_data)):
                cos_n_volume = int((traffic_cos_data[n]/100) * self.volume[t]) # cos n traffic volume
                cos_n_traffic = self.generate_cos_traffic(n, cos_n_volume)
                traffic_t += cos_n_traffic
            #
            shuffle(traffic_t)
            self.traffic.append(traffic_t)
            
            # PROGRESS BAR
            if t == (x*int(len(self.volume)/100)):
                print("TRAFFIC GENERATION PROGRESS IS @ {}%: {}".format(x, x*'='+'>'))
                x+=1


    def generate_cos_traffic(self, cos, volume):

        # Frame Length (FIXED)
        fl = 1538  # Bytes

        # Number of Frames
        nof = volume//fl

        traffic = nof*[[cos, fl]]
        
        return traffic

    