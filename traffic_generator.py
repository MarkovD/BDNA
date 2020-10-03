from random import shuffle, gauss

class TrafficGenerator():
    def __init__(self, throughput, traffic_cos_data):
        """[summary]

            traffic_cos_data:

            |cos0_%   |cos0_ev  |
            |cos1_%   |cos1_ev  |
            |cos2_%   |cos3_ev  |
            |...      |...      |
            |cos7_%   |cos7_ev  |

            Time Resolution = 1s

        Args:
            throughput ([type]): [description]
            traffic_cos_data ([type]): [description]
        """

        #if throughput < 0:
        #    raise Exception("throughput must be positive or zero. It cannot be = {}".format(throughput))
        
        self.throughput = throughput  #bit/s
        self.volume = [int(t/8) for t in self.throughput]   #bytes/s

        self.traffic_cos_data = traffic_cos_data

        self.traffic = []

        for t in range(len(self.volume)):
            
            traffic_t = []
            #
            for n in range(len(traffic_cos_data)):
                cos_n_tv = int((traffic_cos_data[n][0]/100) * self.volume[t]) # cos n target traffic volume
                cos_n_traffic = self.generate_cos_traffic(n, traffic_cos_data[n][1], cos_n_tv)
                traffic_t += cos_n_traffic
            #
            shuffle(traffic_t)
            self.traffic.append(traffic_t)


    def generate_cos_traffic(self, cos, cos_ev, ctv):

        # Remember: min = 64, max = 9000
        mu = cos_ev
        sigma = 0.2*mu

        #initialize cos_traffic matrix
        cos_traffic = []

        while ctv > mu:

            # Generate Frame 
            frame_length = int(abs(gauss(mu,sigma)))  #Bytes

            # frame length must be inside the range [64 9000] 
            if frame_length > 9000:
                frame_length = 9000
            elif frame_length < 64:
                frame_length = 64

            if ctv >= frame_length:
                cos_traffic.append([cos, frame_length])
                ctv-=frame_length
        
        return cos_traffic

    

