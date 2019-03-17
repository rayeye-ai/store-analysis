import os

BASE = "splits"

def main():
    for x in xrange(5):
	count = 0
        with open("list/" + "test01.txt", "a") as test_file:
            with open("list/" + "train01.txt", "a") as train_file:
        	for filename in os.listdir(BASE + "/" + str(x) + "/"):
	    
	    	    print filename

	    	    if count % 4 == 0:

		        test_file.write(str(x) + "/" + filename + "\n")
	            else:
		        train_file.write(str(x) + "/" + filename + "\n")
		    count +=1	
		


if __name__ == "__main__":
    main()
