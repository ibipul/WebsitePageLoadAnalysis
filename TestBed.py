from Analyzer import TestDriver
from Analyzer import analyze
import copy
import json
ab = TestDriver(driver_exec_path = 'c:\\temp\\cse534-master\\cse534-master\\chromedriver.exe',
                extension_path='c:\\temp\\cse534-master\\cse534-master\\extension_3_28_0_0.crx',
                adblock=True)
nab = TestDriver(driver_exec_path = 'c:\\temp\\cse534-master\\cse534-master\\chromedriver.exe',
                 extension_path='c:\\temp\\cse534-master\\cse534-master\\extension_3_28_0_0.crx',
                 adblock=False)
x = analyze(site_file_path='c:\\temp\\cse534-master\\cse534-master\\test_list.txt',ab_driver=ab,nab_driver=nab)
x.get_data()
from collections import defaultdict
object_stat={"fetchStart":[],"duration":[],"requestStart":[],"responseStart":[],"responseEnd":[],
             "transferSize":[],"encodedBodySize":[],"decodedBodySize":[],"resReqDiff":[], "startTime":[],
             "tranEncSizeDiff":[],"EncDecSizeDiff":[],"numberOfObj":0,"totalTranSize":0,
             "totalEncSize":0,"totalDecSize":0,"ParDur":0,"nonParDur":0,"serverWait":0}
def create_stat(objects):
    stats = {}
    i = 0
    while i < len(objects):
        try:
            type = objects[i]["initiatorType"]
            if type in stats:
                stats[type]["fetchStart"].append(objects[i]["fetchStart"])
                stats[type]["duration"].append(objects[i]["duration"])
                stats[type]["requestStart"].append(objects[i]["requestStart"])
                stats[type]["startTime"].append(objects[i]["startTime"])
                stats[type]["responseStart"].append(objects[i]["responseStart"])
                stats[type]["responseEnd"].append(objects[i]["responseEnd"])
                stats[type]["transferSize"].append(objects[i]["transferSize"])
                stats[type]["encodedBodySize"].append(objects[i]["encodedBodySize"])
                stats[type]["decodedBodySize"].append(objects[i]["decodedBodySize"])
                stats[type]["resReqDiff"].append(objects[i]["responseStart"] - objects[i]["requestStart"])
                stats[type]["tranEncSizeDiff"].append(objects[i]["encodedBodySize"] - objects[i]["transferSize"])
                stats[type]["EncDecSizeDiff"].append(objects[i]["decodedBodySize"] - objects[i]["encodedBodySize"])
                stats[type]["numberOfObj"] += 1
                stats[type]["totalTranSize"] += objects[i]["transferSize"]
                stats[type]["totalEncSize"] += objects[i]["encodedBodySize"]
                stats[type]["totalDecSize"] += objects[i]["decodedBodySize"]
                stats[type]["nonParDur"] += objects[i]["responseEnd"]- objects[i]["startTime"]
                stats[type]["serverWait"] += objects[i]["responseStart"] - objects[i]["requestStart"]
                i+=1
            else:
                stats.update({type:copy.deepcopy(object_stat)})
        except:
            i+=1
            continue
    for key in stats:
        stats[key]["ParDur"] = max(stats[key]["responseEnd"])- min(stats[key]["startTime"])
    return stats

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
stat_ab = []
stat_nab = []
for i in range(0, len(x.website_objs)):
    e = x.website_objs[i]
    print('Website:: ', e.name)
    r_ab = len(e.components_wtblock)
    r_nab = len(e.components_normal)
    '''Calculation statistics'''
    stat_ab =create_stat(e.components_wtblock)
    stat_nab = create_stat(e.components_normal)
    # print('Req count: wt AB: ', r_ab, ' wt Nab: ', r_nab)
    # s_ab = size_computation(e.components_wtblock)
    # s_nab = size_computation(e.components_normal)
    # print('Size: wt AB: ', s_ab, ' wt Nab: ', s_nab, 'diff: ', s_nab - s_ab)
    # p_ab = first_meaningful_paint(e.components_wtblock)
    # p_nab = first_meaningful_paint(e.components_normal)
    # print('Paint: wt AB: ', p_ab, ' wt Nab: ', p_nab, 'diff: ', p_nab - p_ab)
    # t_ab = max_timestamp(e.components_wtblock)
    # t_nab = max_timestamp(e.components_normal)
    # print('Last Seen: wt AB: ', t_ab, ' wt Nab: ', t_nab, 'diff: ', t_nab - t_ab)
    # b_ab = object_breakup(e.components_wtblock)
    # b_nab = object_breakup(e.components_normal)
    # #diff_n = (b_nab['navigation'] - b_ab['navigation'])*100/b_ab['navigation']
    # #diff_r = (b_nab['resource'] - b_ab['resource'])*100/b_ab['resource']
    # print("navigation: wt AB ",b_ab['navigation']*100, " wt Nab: ", b_nab['navigation']*100)# 'diff: ', diff_n)
    # print("resource: wt AB ", b_ab['resource']*100, " wt Nab: ", b_nab['resource']*100)#, 'diff: ', diff_r)
    print "Processing done for ", e.name
    try:
        dc = {'name': e.name,
				'nav_ab_par':stat_ab['navigation']['ParDur'], 'nav_ab_npar':stat_ab['navigation']['nonParDur'], 'nav_ab_sh_wait':stat_ab['navigation']['serverWait'],
								'nav_ab_num_obj':stat_ab['navigation']['numberOfObj'], 'nav_ab_tran_size':stat_ab['navigation']['totalTranSize'], 'nav_ab_enc_size':stat_ab['navigation']['totalEncSize'], 'nav_ab_dec_size':stat_ab['navigation']['totalDecSize'],
			   'css_ab_par':stat_ab['css']['ParDur'], 'css_ab_npar':stat_ab['css']['nonParDur'], 'css_ab_sh_wait':stat_ab['css']['serverWait'],
								'css_ab_num_obj':stat_ab['css']['numberOfObj'], 'css_ab_tran_size':stat_ab['css']['totalTranSize'], 'css_ab_enc_size':stat_ab['css']['totalEncSize'], 'css_ab_dec_size':stat_ab['css']['totalDecSize'],
			   'script_ab_par':stat_ab['script']['ParDur'], 'script_ab_npar':stat_ab['script']['nonParDur'],'script_ab_sh_wait':stat_ab['script']['serverWait'],
								'script_ab_num_obj':stat_ab['script']['numberOfObj'], 'script_ab_tran_size':stat_ab['script']['totalTranSize'], 'script_ab_enc_size':stat_ab['script']['totalEncSize'], 'script_ab_dec_size':stat_ab['script']['totalDecSize'],
			   #'iframe_ab_par':stat_ab['iframe']['ParDur'], 'iframe_ab_npar':stat_ab['iframe']['nonParDur'],'sh_wait':stat_ab['iframe']['serverWait'],
			   'img_ab_par':stat_ab['img']['ParDur'], 'img_ab_npar':stat_ab['img']['nonParDur'],'img_ab_sh_wait':stat_ab['img']['serverWait'],
								'img_ab_num_obj':stat_ab['img']['numberOfObj'], 'img_ab_tran_size':stat_ab['img']['totalTranSize'], 'img_ab_enc_size':stat_ab['img']['totalEncSize'], 'img_ab_dec_size':stat_ab['img']['totalDecSize'],
			   'link_ab_par':stat_ab['link']['ParDur'], 'link_ab_npar':stat_ab['link']['nonParDur'],'link_ab_sh_wait':stat_ab['link']['serverWait'],
								'link_ab_num_obj':stat_ab['link']['numberOfObj'], 'link_ab_tran_size':stat_ab['link']['totalTranSize'], 'link_ab_enc_size':stat_ab['link']['totalEncSize'], 'link_ab_dec_size':stat_ab['link']['totalDecSize'],
				'nav_nab_par':stat_nab['navigation']['ParDur'], 'nav_nab_npar':stat_nab['navigation']['nonParDur'], 'nav_nab_sh_wait':stat_nab['navigation']['serverWait'],
								'nav_nab_num_obj':stat_nab['navigation']['numberOfObj'], 'nav_nab_tran_size':stat_nab['navigation']['totalTranSize'], 'nav_nab_enc_size':stat_nab['navigation']['totalEncSize'], 'nav_nab_dec_size':stat_nab['navigation']['totalDecSize'],
				'css_nab_par':stat_nab['css']['ParDur'], 'css_nab_npar':stat_nab['css']['nonParDur'], 'css_nab_sh_wait':stat_nab['css']['serverWait'],
								'css_nab_num_obj':stat_nab['css']['numberOfObj'], 'css_nab_tran_size':stat_nab['css']['totalTranSize'], 'css_nab_enc_size':stat_nab['css']['totalEncSize'], 'css_nab_dec_size':stat_nab['css']['totalDecSize'],
			   'script_nab_par':stat_nab['script']['ParDur'], 'script_nab_npar':stat_nab['script']['nonParDur'],'script_nab_sh_wait':stat_nab['script']['serverWait'],
								'script_nab_num_obj':stat_nab['script']['numberOfObj'], 'script_nab_tran_size':stat_nab['script']['totalTranSize'], 'script_nab_enc_size':stat_nab['script']['totalEncSize'], 'script_nab_dec_size':stat_nab['script']['totalDecSize'],
			   #'iframe_nab_par':stat_nab['iframe']['ParDur'], 'iframe_nab_npar':stat_nab['iframe']['nonParDur'],'sh_wait':stat_nab['iframe']['serverWait'],
			   'img_nab_par':stat_nab['img']['ParDur'], 'img_nab_npar':stat_nab['img']['nonParDur'],'img_nab_sh_wait':stat_nab['img']['serverWait'],
								'img_nab_num_obj':stat_nab['img']['numberOfObj'], 'img_nab_tran_size':stat_nab['img']['totalTranSize'], 'img_nab_enc_size':stat_nab['img']['totalEncSize'], 'img_nab_dec_size':stat_nab['img']['totalDecSize'],
			   'link_nab_par':stat_nab['link']['ParDur'], 'link_nab_npar':stat_nab['link']['nonParDur'],'link_nab_sh_wait':stat_nab['link']['serverWait'],
								'link_nab_num_obj':stat_nab['link']['numberOfObj'], 'link_nab_tran_size':stat_nab['link']['totalTranSize'], 'link_nab_enc_size':stat_nab['link']['totalEncSize'], 'link_nab_dec_size':stat_nab['link']['totalDecSize'],
			  }
        jlist.append(dc)
    except Exception:
        print "some error"
        continue
    with open('web_data.txt', 'a') as outfile:
        json.dump(jlist, outfile)

import csv

keys = jlist[0].keys()
with open('website_stat_comparison.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(jlist)

#
#with open('web_data.txt', 'w') as outfile:
#    json.dump(jlist, outfile)

