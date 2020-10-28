import speedtest
import time
import threading

waitTime = 60 # Timestep in seconds to wait between measurements
columns =  ["time pre","time middle","time post","download (Mbps)","upload (Mbps)"]

lock = threading.Lock()

def main():
	st = speedtest.Speedtest()
	t0 = time.time()

	fName = "speedLog-%d.txt"%t0

	print "Saving data as " + fName

	# Get best server and log info
	f = open(fName,"w")
	server = st.get_best_server()

	for s in server:
		f.write("# " + s + "\t" + str(server[s]) + "\n")
	f.write("# " + '\t'.join(columns) + "\n")
	f.close()

	t = threading.Thread(target=logSpeed,args=(fName,st))
	t.daemon=True
	t.start()

	raw_input("Press Enter to quit.")


def logSpeed(fName,st):
	while(True):
		lock.acquire()

		# Get dl/ul speeds and 3 times pre/middle/post measurement	
		t1 = time.time()
		dl = st.download()
		t2 = time.time()
		ul = st.upload()
		t3 = time.time()

		# Save data and close file
		f = open(fName,"a+")
		f.write("%f\t%f\t%f\t%f\t%f\n"%(t1,t2,t3,dl,ul))
		f.close()

		lock.release()

		# Wait for specified timestep
		time.sleep(waitTime)


if __name__ == "__main__":
    main()


