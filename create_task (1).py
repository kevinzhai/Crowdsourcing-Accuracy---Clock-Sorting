from __future__ import division
import sys
import itertools as it
import random

if __name__ == '__main__' :
    
    if len(sys.argv) < 2 : print "Usage: python create_task.py  task=create_task or validate  validation_file" ; exit(0)
    clocks = open('times_and_urls.txt', 'r')
    task = sys.argv[1]
    # if there is a third argument, set it to the length of the url combinations
    urls_and_times = {}
    # add urls and times to dict
    for line in clocks:
        time, url = tuple(line.split(","))
        url = url.strip()
        if time not in ["NA", "N/A"]:
            time = float(time)
            urls_and_times[url] = time
    # create combinations of urls
    if task == 'create_task':
        url_combos = random.shuffle(list(it.combinations(urls_and_times, n)))
        url_combos = url_combos[:37000]
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
        for urls in final_url_combo_list:
            f.write(','.join(urls) + '\n')
        f.close()

    elif task == 'validate':
        v = open(sys.argv[2], 'r')
        total_valid_responses = 0
        correct_responses = 0
        skipped_too_close = 0
        for line in v:
            id, first, third, second, url_1, url_2, url_3 = tuple(line.split(','))
            url_1, url_2, url_3 = url_1.strip(), url_2.strip(), url_3.strip()
            crowd_answer = first + second + third
            try:
                time_list = [urls_and_times[url_1], urls_and_times[url_2], urls_and_times[url_3]]
            except KeyError, e:
                print e
                continue
            sorted_times = sorted(time_list)
            if sorted_times[1] - sorted_times[0] < .05 or sorted_times[2] - sorted_times[1] < .05:
                skipped_too_close += 1
                continue
            total_valid_responses += 1
            our_answer = ""
            if time_list[0] == sorted_times[0]: our_answer += "a"
            elif time_list[1] == sorted_times[0]: our_answer += "b"
            else: our_answer += "c"
            if time_list[0] == sorted_times[1]: our_answer += "a" 
            elif time_list[1] == sorted_times[1]: our_answer += "b"
            else: our_answer += "c"
            our_answer += next(iter(set("abc") - set(our_answer)))
            if crowd_answer != our_answer:
                print id, crowd_answer, our_answer
            if crowd_answer == our_answer:
                correct_responses += 1
        print "total skipped because too close: " + str(skipped_too_close)
        print "correct: ", str(correct_responses/total_valid_responses), "% ", "total answered: ", total_valid_responses, "total correct: ", correct_responses 

