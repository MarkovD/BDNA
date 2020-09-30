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

        self.cos0_traffic = []
        self.cos1_traffic = []
        self.cos2_traffic = []

        self.traffic = []

    def greedy_generation(cos, cos_ev, ctf):
        # Almost-Gaussian Distribution
        # Remember: min = 64, max = 9000
        mu = cos_ev
        sigma = mu*(1+)

        #init sequence
        sequence = []

        while ctf is >= 64
        # Generate value 
        packet_length = random.gauss()
        # if value < cos_target_volume (ctf)
        # add value to sequence
        # Decrement ctf: ctf = ctf - value

        # return cos_matrix:
        # | cos | value1 |
        # | cos | value2 |
        # | cos | ecc    |
