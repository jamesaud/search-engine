import sys
import os
import random
# from Queue import PriorityQueue
from operator import itemgetter
from subprocess import call

# Summary:
# So what we did here was try to find a solution by using scrapy
# in the terminal, but still allowing the use of variables. This was really difficult
# to figure out how to get this to work and it probably isn't the best solution
# but it does work. We save the variables from the input in a temp text document
# and from our other code retrieve the data.
if __name__ == '__main__':

    if len(sys.argv) != 5:
        print "Need more Args"
        sys.exit()

    file = open('temp_global_settings.txt', 'w')

    file.write(sys.argv[1]+"\n")
    file.write(sys.argv[2]+"\n")
    file.write(sys.argv[3]+"\n")
    file.write(sys.argv[4]+"\n")

    file.close()

    if sys.argv[4] == "dfs":
        os.system("scrapy crawl dfs")
    elif sys.argv[4] == "bfs":
        os.system("scrapy crawl bfs")
    else:
        print("Not supported search type")
