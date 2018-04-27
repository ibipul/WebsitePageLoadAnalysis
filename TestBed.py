from Analyzer import TestDriver
from Analyzer import analyze
ab = TestDriver(driver_exec_path = 'C:\\Users\\ibipul\\chromedriver.exe',
                extension_path='C:\\Users\\ibipul\\codes\\cse534\\extension_3_28_0_0.crx',
                adblock=True)
nab = TestDriver(driver_exec_path = 'C:\\Users\\ibipul\\chromedriver.exe',
                 extension_path='C:\\Users\\ibipul\\codes\\cse534\\extension_3_28_0_0.crx',
                 adblock=False)
x = analyze(site_file_path='C:\\Users\\ibipul\\codes\\cse534\\test_list.txt',ab_driver=ab,nab_driver=nab)
x.get_data()
from collections import defaultdict
def size_computation(components):
    sum=0
    for x in components:
        if 'decodedBodySize' in x.keys():
            sum+=x['decodedBodySize']
    return sum
def first_meaningful_paint(components):
    l=[0]
    for x in components:
        if x['entryType'] =='paint':
            l.append(x['startTime'])
    return max(l)
def max_timestamp(components):
     l = [0]
     for x in components:
         l.append(x['startTime'])
     return max(l)
def object_breakup(components):
    tot=len(components)
    d = defaultdict(int)
    for x in components:
        d[x['entryType']]+=1
    for k in d.keys():
        d[k] = d[k]/tot
    return d
jlist = []
for i in range(0, len(x.website_objs)):
    e = x.website_objs[i]
    print('Website:: ', e.name)
    r_ab = len(e.components_wtblock)
    r_nab = len(e.components_normal)
    print('Req count: wt AB: ', r_ab, ' wt Nab: ', r_nab)
    s_ab = size_computation(e.components_wtblock)
    s_nab = size_computation(e.components_normal)
    print('Size: wt AB: ', s_ab, ' wt Nab: ', s_nab, 'diff: ', s_nab - s_ab)
    p_ab = first_meaningful_paint(e.components_wtblock)
    p_nab = first_meaningful_paint(e.components_normal)
    print('Paint: wt AB: ', p_ab, ' wt Nab: ', p_nab, 'diff: ', p_nab - p_ab)
    t_ab = max_timestamp(e.components_wtblock)
    t_nab = max_timestamp(e.components_normal)
    print('Last Seen: wt AB: ', t_ab, ' wt Nab: ', t_nab, 'diff: ', t_nab - t_ab)
    b_ab = object_breakup(e.components_wtblock)
    b_nab = object_breakup(e.components_normal)
    diff_n = (b_nab['navigation'] - b_ab['navigation'])*100/b_ab['navigation']
    diff_r = (b_nab['resource'] - b_ab['resource'])*100/b_ab['resource']
    print("navigation: wt AB ",b_ab['navigation']*100, " wt Nab: ", b_nab['navigation']*100, 'diff: ', diff_n)
    print("resource: wt AB ", b_ab['resource']*100, " wt Nab: ", b_nab['resource']*100, 'diff: ', diff_r)
    dc = {'name': e.name,
          'req_AB':r_ab, 'req_NAB': r_nab,
          'dwnld_AB':s_ab, 'dwnld_NAB': s_nab,
          'paint_AB':p_ab, 'paint_NAB': p_nab,
          'last_ts_AB':t_ab, 'last_ts_NAB':t_nab,
          'nav_traff_perc_AB': b_ab['navigation']*100, 'nav_traff_perc_NAB': b_nab['navigation']*100,
          'resource_dwnld_AB': b_ab['resource']*100, 'resource_dwnld_NAB': b_nab['resource']*100
          }
    jlist.append(dc)

import csv

keys = jlist[0].keys()
with open('website_stat_comparison.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jlist)

import json
with open('web_data.txt', 'w') as outfile:
    json.dump(jlist, outfile)

