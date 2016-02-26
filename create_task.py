import sys
import itertools as it
import random  




if __name__ == '__main__' :
    
    if len(sys.argv) < 2 : print "Usage: python create_task.py URLS_AND_TIMES IMAGES_PER_SET"; exit(0)
    clocks = open(sys.argv[1], 'r')
    # if there is a third argument, set it to the length of the url combinations
    n = 3
    if len(sys.argv) > 2:
        n = int(sys.argv[2])
    urls_and_times = {}
    # add urls and times to dict
    i = 0
    for line in clocks:
        i+=1
        time, url = tuple(line.split(','))
        if time not in ["NA", "N/A"]:
            time = float(time)
            urls_and_times[url] = time
    # create combinations of urls
    times_array = []
    for key in urls_and_times:
        times_array.append(key.rstrip())

    list_of_url_pairs = []
    for i in range(1,10000):
        list_of_url_pairs.append(str(times_array[random.randint(0, len(times_array)) - 1]) + ', ' + str(times_array[random.randint(0, len(times_array))- 1]) + ', ' + str(times_array[random.randint(0, len(times_array)) - 1]))


    url_combos = it.combinations(urls_and_times, n)
    final_url_combo_list = []
    # for each combination of urls, make sure no two times are within five minutes of each other
    for combo in url_combos:
        times = sorted([urls_and_times[url] for url in combo])
        too_close = False
        for i, time in enumerate(times):
            if i != len(times) - 1:
                if times[i+1] - times[i] < .05:
                    too_close = True
        if not too_close:
            final_url_combo_list.append(combo)
    
    f = open('clock_combos.txt', 'w')
    for urls in list_of_url_pairs:
        f.write(urls + '\n')
    f.close()
