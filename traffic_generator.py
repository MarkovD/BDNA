
class TrafficGenerator():
    def __init__(throughput, traffic_distribution):
        """[summary]

            traffic_distribution:
            |cos0_%   |cos0_ev  |
            |cos3_%   |cos1_ev  |
            |cos5_%   |cos3_ev  |

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
        self.cos3_percent = self.td[2][0]
        self.cos3_ev = self.td[2][1]

        self.volume = throughput/8  #Bytes/s
        self.cos0_target_volume = self.cos0_percent * self.volume
        self.cos1_target_volume = self.cos1_percent * self.volume
        self.cos3_target_volume = self.cos3_percent * self.volume

    def greedy_generation(cos, cos_ev, cos_target_volume):
        # Almost-Gaussian Distribution
        # Remember: min = 64, max = 9000
        # mu = cos_ev
        # sigma = mu + 25%*mu

        #init sequence
        sequence = []
        # while ctf is >= 64
        # Generate value 
        # if value < cos_target_volume (ctf)
        # add value to sequence
        # Decrement ctf: ctf = ctf - value

        # return cos_matrix:
        # | cos | value1 |
        # | cos | value2 |
        # | cos | ecc    |

