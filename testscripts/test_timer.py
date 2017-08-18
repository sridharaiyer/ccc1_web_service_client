import time
timeout = time.time() + 5   # 5 seconds from now
i = 0
while True:
    if i == 5 or time.time() > timeout:
        break
    print('Hello')
    time.sleep(1)
    i += 1
