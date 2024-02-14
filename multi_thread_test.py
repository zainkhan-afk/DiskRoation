from test_api import TestAPI
import threading


NUM_TESTS = 20

threads = []

for i in range(NUM_TESTS):
	t = threading.Thread(target = TestAPI)
	threads.append(t)


print("Starting threads")
for t in threads:
	t.start()
