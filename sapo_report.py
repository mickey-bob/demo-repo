import csv
import re
from collections import Counter
import os

# file_import = "/home/khanhnt2/Desktop/data/data-main/note-sapo/python/python-for-devops/khanhnt2/sapo_report/1.csv"
report_dir = "/home/khanhnt2/Desktop/sapo-report/week"
current_dir = os.getcwd()

def open_one_file(sapo_file_report, info_track=None):
  num_count = 0
  with open(sapo_file_report, 'r') as f:
    sapo_domain_monitor = {}
    output = csv.reader(f, delimiter=',')
    for x_line in output:
      if num_count == 0:
        # remove first row
        num_count += 1
        continue
      x_line[-1] = int(x_line[-1].replace(',',''))
      if x_line[0] in sapo_domain_monitor.keys():
        sapo_domain_monitor[x_line[0]][2] += x_line[3]
      else:
        sapo_domain_monitor[x_line[0]] = x_line[1:]
      
  return sapo_domain_monitor

    
    
def combine_dicts_to_csv(sum_dicts, count_dict):
  result_list = []
  for k,v in sum_dicts.items():
    # reset sum_dict every loops, sum_dict will get new value --> result_list will be update
    sum_dict = {}
    # .....
    sum_dict['Domain'] = k
    sum_dict['Method'] = v[0]
    sum_dict['IP'] = v[1]
    sum_dict['Total_request_scan'] = v[2]
    sum_dict['Times_attack'] = count_dict[k]
    result_list.append(sum_dict)
  return result_list


def fun_count_world(world):
  count_world = Counter()
  count_world.update(world)
  return count_world

# x = open_one_file(sapo_file_report='/home/khanhnt2/Desktop/data/data-main/note-sapo/python/python-for-devops/khanhnt2/sapo_report/1.csv')
# print(x)

# initiate count variable
count_domain = Counter()


# change to report dir, and do some logic
os.chdir(report_dir)

sum_results = {}

for file_name in os.listdir('./'):
  if file_name.endswith('.csv'):
    results = open_one_file(sapo_file_report=file_name)
    while len(results) > 0:
      pop_result = results.popitem()
      if pop_result[0] not in sum_results.keys():
        sum_results[pop_result[0]] = pop_result[1]
        # print(pop_result[0])
        count_domain[pop_result[0]] += 1
      else:
        sum_results[pop_result[0]][2] += pop_result[1][2]
        count_domain[pop_result[0]] += 1
        # print(pop_result[0])
        
      

# print(sum_results)
# print('=='*40)
# print(count_domain)
# print('=='*40)

    
# combine dict: sum_results vs dict: count_domain
os.makedirs('./results', exist_ok=True)
os.chdir('./results')
list_dict_to_csv = combine_dicts_to_csv(sum_dicts=sum_results, count_dict= count_domain)
headers = ['Domain', 'Method', 'IP', 'Total_request_scan', 'Times_attack']
print(list_dict_to_csv)
with open('./result.csv', 'w' ,newline='\n') as f:
  output = csv.DictWriter(f, fieldnames=headers)
  output.writeheader()
  output.writerows(list_dict_to_csv)

# change back to current dir - running app
os.chdir(current_dir)

