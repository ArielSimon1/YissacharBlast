#!/usr/bin/env python
import sys
import os
import itertools
import operator

def get_ids(results_file):
    res = open(results_file)
    check = 0
    id_dict = {}
    for line in res:
        if line.startswith("Query="):
            id = line[7:35].strip()
            if id not in id_dict.keys():
                id_dict[id] = {}
            check = 1
    res.close()
    if check == 0:
        print("there is no sequence IDs")
        exit(0)
    return id_dict

def get_taxon(results_file, id_dict):
    taxon_dict = {}
    counter = 0
    res = open(results_file)
    for value in id_dict:
        taxon_dict[value] = {}
        for line in res:
            if line.__contains__(value):
                counter = counter + 1
                res.readline()
                res.readline()
                res.readline()
                res.readline()
                res.readline()
                for x in range(9):
                    new_line = res.readline()
                    taxon = new_line.strip()
                    tmp = new_line.split()
                    taxon_dict[value][taxon] = [tmp[1], tmp[2]]


    res.close()
    return taxon_dict, counter

def get_precents(taxon_dict):
    precents_dict = {}
    for taxa in taxon_dict.values():
        for ids in taxa.values():
            precents_dict[taxa.values()] = {}
            precents_dict[taxa.values()] = [ids]
    return precents_dict

def most_common(list):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(list))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(list)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


########## MAIN ##########
# usage check
if (len(sys.argv) < 2):
    print("Usage example: python3 blastn_checker.py [blastn results file name]")
    exit(1)

# input file check
isExist = os.path.exists(sys.argv[1])
if (isExist == False):
    print("the file name isn't exists.")
    exit(1)

# set the input file
resultsFile = sys.argv[1]
id_dict = get_ids(resultsFile)
print("The ID you chose are: ")
for value in id_dict:
   print(value, "is:")



taxons, counter = get_taxon(resultsFile, id_dict)
print(counter)
# get_precents
list = []
check = get_precents(taxons)
for value in check.values():
        list.append(value)
#print(list)

#for i in range(len(list)):
 #   x = bool(list[i])
    # if x == False:
  #     del list[i]
      #   i = i+1
#print(list)
#print(type(list))
#print(most_common(list))

#keys = Counter(check.values())
#mode = keys.most_common(1)


#for value in taxons:
 #   for value in taxons.values():
  #      print(value.values())
#print("The identification based on blastn results are: ")
#for value in taxons.keys():
  #print(value)

