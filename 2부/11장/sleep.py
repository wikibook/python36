import time
t = time.time()
time.sleep(10)
t2 = time.time()

spendtime = t2 - t
print("Before timestemp: ", t)
print("After timestemp: ", t2)
print("Wait {0} seconds".format(spendtime))