import sys,time

if __name__=="__main__":
    print sys.version
    t1 = time.time() # start time
    N = 5000000
    # init
    sieve = {}
    for i in range(2, N+1):
        sieve[i] = 0
    # Sieve of Eratosthenes
    for i in range(2, N+1):
        if sieve[i]==0:
            n=2
            while i*n <= N:
                sieve[i*n]=1
                n+=1
    # print results count
    cnt = 0
    for i in range(2, N+1):
        if sieve[i]==0:
            cnt += 1
    t2 = time.time() # end time
    print cnt
    print "elapsed time=", t2-t1, " sec"