from random import randrange, randint, seed
seed()

def main():
    seq = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    seq = [i for i in range(randint(0,1000001))]
    print(len(seq))
    oom = morris_algo(seq)
    print(oom)

def morris_algo(sequence):
    
    order_of_magnitude = 0

    i=0
    while i < len(sequence):
        
        random_int = randrange(10**order_of_magnitude)
        
        if random_int == 0:
            order_of_magnitude += 1
        
        i+=1

    return order_of_magnitude

if __name__ == "__main__":
    main()