from random import gauss
from math import sqrt

class TrafficGenerator():
    def __init__(throughput, traffic_distribution):
        """[summary]

            traffic_distribution:
            |cos0_%   |cos0_ev  |
            |cos1_%   |cos1_ev  |
            |cos2_%   |cos3_ev  |

            Time Resolution = 1s

        Args:
            throughput ([type]): [description]
            traffic_distribution ([type]): [description]
        """

        self.throughput = throughput  #bit/s
        self.td = traffic_distribution
        
        self.cos0_percent = self.td[0][0]
        self.cos0_ev = self.td[0][1]
        self.cos1_percent = self.td[1][0]
        self.cos1_ev = self.td[1][1]
        self.cos2_percent = self.td[2][0]
        self.cos2_ev = self.td[2][1]

        self.volume = throughput/8  #Bytes/s
        self.cos0_target_volume = self.cos0_percent * self.volume
        self.cos1_target_volume = self.cos1_percent * self.volume
        self.cos2_target_volume = self.cos2_percent * self.volume

        self.cos0_traffic = self.greedy_generation(0, self.cos0_ev, self.cos0_target_volume)
        self.cos1_traffic = self.greedy_generation(1, self.cos1_ev, self.cos1_target_volume)
        self.cos2_traffic = self.greedy_generation(2, self.cos2_ev, self.cos2_target_volume)

        self.traffic = []

    def greedy_generation(cos, cos_ev, ctf):
        # Almost-Gaussian Distribution
        # Remember: min = 64, max = 9000
        mu = cos_ev
        sigma = 1.2*mu

        #init cos matrix
        cos_matrix = []

        while ctf >= 64:

            # Generate random length frame 
            frame_length = random.gauss(mu,sigma)  #Bytes

            # frame length must be inside the range [64 9000] 
            if packet_length > 9000:
                packet_length = 9000
            elif packet_length < 64:
                packet_length = 64

            if packet_length > (ctf-64):
                packet_length=ctf-64
            
            cos_matrix.append([cos, packet_length])
            ctf-=packet_length
        
        return cos_matrix


