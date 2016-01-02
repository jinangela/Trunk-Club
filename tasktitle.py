#!/usr/bin/env python
# first run the following command in terminal:
# pip install stop-words

import os
import re # regex
import numpy as np
import string
import itertools
import collections
from stop_words import get_stop_words

def tokenization(dict,punct,drop = []):
	# tokenize the values in dict
	# punct specifies how you want to split the sentences
	# drop gives you a list of the words that you want to drop after tokenization
	split_results = {}
	replace = string.maketrans(punct, " "*len(punct)) # replace all characters in punct with blanks
	for key in dict:
		split_results[key] = [x for x in dict[key].translate(replace).split() if x not in drop]
	return split_results

def dict_list_freq_count(dict):
	count_dict = {}
	for key in dict:
		for word in dict[key]:
			if word in count_dict:
				count_dict[word] += 1
			else:
				count_dict[word] = 1
	return count_dict

def dict_frequency_count(dict):
	count_dict = {}
	for key in dict:
		if dict[key] in count_dict:
			count_dict[dict[key]] += 1
		else:
			count_dict[dict[key]] = 1
	return count_dict

def list_frequency_count(list):
	count_dict = {}
	for word in list:
		if word in count_dict:
			count_dict[word] += 1
		else:
			count_dict[word] = 1
	return count_dict

tasktitle = {} # a dictionary, taskid is the key
stylist = {} # dictionary of the stylistinitiatedindicator, taskid is the key
# use it to check if the task was initiated by a stylist or not(so the tasktitle will be free form)
fc_id = {} # dictionary of the featuredcollections, taskid is the key

word_list = set() # If we use a set, looking up a word in the word_list might be more efficient
# The following dictionary of English words seems to be useful. Feel free to modify it.
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\list of english words.txt",'r') as file:
	for line in file:
		word_list.add(line.rstrip())

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\tasktitle.txt",'r') as file:
	file.readline() # skip the first line(column names)
	
	for line in file:
		line = line.replace('"', '') # remove double quotes
		stylist[line.split('\t')[1]] = line.split('\t')[2] # 0 or 1 or NA
		tasktitle[line.split('\t')[1]] = line.split('\t')[3].rstrip() # use .rstrip to remove newline character
		fc_id[line.split('\t')[1]] = line.split('\t')[4] # featured collections number(s) or null

# divide the tasktitle into five categories according to the new trunk club bible
tasktitle_result = {}
blank = {} # member initiated and tasktitle is blank -> message request
temp = {} # the other four categories
member = {} # used to differentiate different types of member initiated requests	
for key in tasktitle:
	if tasktitle[key] == "":
		blank[key] = tasktitle[key]
	else:
		temp[key] = tasktitle[key]

tasktitle_result["blank"] = blank

featuredcollections = {} # featured collections(initials in capitals for each word in tasktitle) -> page specific request
csc = {} # comma separated categories -> old trunk request system
stylistinitiated = {} # stylistinitiatedindicator == 1 -> stylist initiated request
others = {} # for those tasktitles that stylistinitiatedindicator == 0 but are still in free form

# 1. word tokenization: translate all punctuations except underscore and single quote into blank to split words from tasktitles in temp
punct = string.punctuation.translate(None,"_'") # None means only delete underscore and single quotation mark from string.punctuation
drop = ["_","'"]
not_blank_tokens = tokenization(temp,punct,drop)

# 2. output all the tasktitles having words that are not in the dictionary of English words to see if there are any abbreviations
# need to be corrected first(the following file "not in the dictionary.txt" can be used to check the contexts when not sure what the abbreviations mean)
abbr = []
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\not in the dictionary.txt",'w') as file:
	for key in not_blank_tokens:
		temp_result = [tasktitle[key]]
		for word in not_blank_tokens[key]:
			if word.lower() not in word_list:
				if word.isdigit() == False and len(word) <= 4:
					abbr.append(word)
					temp_result.append(word)
		if len(temp_result) > 1:
			file.write(key + '\t' + str(temp_result) + '\n')

# do frequency count to rewrite the top n abbreviations to their full names
abbr_count = sorted(list_frequency_count(abbr).items(), key=lambda x: (x[1],x[0]), reverse = True) # descending order; this is a tuple
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\abbreviations_count.txt",'w') as file:
	for i in range(len(abbr_count)):
		file.write(abbr_count[i][0] + '\t' + str(abbr_count[i][1]) + '\n')

# use regular expression to match the most common abbreviations, modify them as full names and then retokenization(Note: capital letters should also be corrected)
for key in temp:
	temp[key] = re.sub(r"\b[Ff][\/.]?[Uu][.p]?\b","follow up",temp[key])
	temp[key] = re.sub(r"\b[Ff][.]?[Uu][.]?[Tt]\b","follow up trunk",temp[key])
	temp[key] = re.sub(r"\b[Uu][Pp][Tt]\b","up trunk",temp[key])
	temp[key] = re.sub(r"\bfollowup\b","follow up",temp[key])
	temp[key] = re.sub(r"\b1st\b","first",temp[key])
	temp[key] = re.sub(r"\b2nd\b","second",temp[key])
	temp[key] = re.sub(r"\b3rd\b","third",temp[key])
	temp[key] = re.sub(r"\b4th\b","fourth",temp[key])
	temp[key] = re.sub(r"\b6\b","Six",temp[key])
	temp[key] = re.sub(r"\b[Bb][Bb][Qq]\b","barbecue",temp[key])
	temp[key] = re.sub(r"\b[Cc][Aa][li]?\b","california",temp[key])
	temp[key] = re.sub(r"\b[Nn][Yy][Cc]?\b","new york",temp[key])
	temp[key] = re.sub(r"\b[Dd][Cc]\b","washington_dc",temp[key])
	temp[key] = re.sub(r"\bSt\b","street",temp[key])
	temp[key] = re.sub(r"\b[Mm][Pp]\b","my pleasure",temp[key])
	temp[key] = re.sub(r"\b[Dd][Ll]\b","dl1961",temp[key])
	temp[key] = re.sub(r"\b[Ww][\/]?\b","with",temp[key])
	temp[key] = re.sub(r"\b[Tt][Pp]\b","top",temp[key])
	temp[key] = re.sub(r"\b[Tt][\ \-]?[Ss]hirt\b","teeshirt",temp[key])
	temp[key] = re.sub(r"\b[Tt]\'s\b","tees",temp[key])
	temp[key] = re.sub(r"\bCo\.\b","company",temp[key])
	temp[key] = re.sub(r"\b[Bb]day\b","birthday",temp[key])
	temp[key] = re.sub(r"\b[Rr][Vv][Yy][Cc]\b","royal vancouver yacht club",temp[key])
	temp[key] = re.sub(r"\b[Vv]aca\b","vacation",temp[key])
	temp[key] = re.sub(r"\b[Dd]igi\b","digital",temp[key])
	temp[key] = re.sub(r"\b[Oo][Pp][Pp]\b","opportunity",temp[key])
	temp[key] = re.sub(r"\b[Ll][Bb][Mm]\b","little big man",temp[key])
	temp[key] = re.sub(r"\b[Aa][Pp][Pp][Tt]\b","appointment",temp[key])
	temp[key] = re.sub(r"\breq[s]?\b","requests",temp[key])
	temp[key] = re.sub(r"\b[Aa][Ss][Aa][Pp]\b","as soon as possible",temp[key])
	temp[key] = re.sub(r"\bAC\b","activity check",temp[key])
	temp[key] = re.sub(r"\b[Vv][Dd]ay\b","valentine day",temp[key])
# I didn't rewrite "SP" and "MT" because I don't think they will provide any insights

# 3. remove stopwords(strategy: if the word is in the list of stop-words, remove it)
stop_words = get_stop_words('english')
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\stop words.txt",'w') as file:
	for i in range(len(stop_words)):
		file.write(str(stop_words[i]) + '\n')

stop_words = [] # I read it again because I don't know how to encode and decode the unicode strings in the original stop_words
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\stop words.txt",'r') as file:
	for line in file:
		stop_words.append(line.rstrip())

# retokenization
not_blank_tokens = tokenization(temp,punct,drop)

for key in not_blank_tokens:
	for word in stop_words:
		while word in not_blank_tokens[key]:
			not_blank_tokens[key].remove(word)

# 4. use levenshtein distance to correct misspelled words
# 4.1. do frequency count to generate a dictionary
count_list = dict_list_freq_count(not_blank_tokens)

# 4.2. calculate levenshtein distances for each word in each list of the whole dictionary not_blank_tokens
# quoted from wikibooks, 5th version, using numpy
def levenshtein(source, target):
	if len(source) < len(target):
		return levenshtein(target, source)
	
	# So now we have len(source) >= len(target).
	if len(target) == 0:
		return len(source)
	
	# We call tuple() to force strings to be used as sequences
	# ('c', 'a', 't', 's') - numpy uses them as values by default.
	source = np.array(tuple(source))
	target = np.array(tuple(target))
	
	# We use a dynamic programming algorithm, but with the added optimization that 
	# we only need the last two rows of the matrix.
	previous_row = np.arange(target.size + 1)
	for s in source:
		# Insertion (target grows longer than source):
		current_row = previous_row + 1
		
		# Substitution or matching:
		# Target and source items are aligned, and either
		# are different (cost of 1), or are the same (cost of 0).
		current_row[1:] = np.minimum(
				current_row[1:],
				np.add(previous_row[:-1], target != s))
		
		# Deletion (target grows shorter than source):
		current_row[1:] = np.minimum(
				current_row[1:],
				current_row[0:-1] + 1)
		
		previous_row = current_row
	
	return previous_row[-1]

# create our dictionary for comparison
dict_list = []
for key in count_list:
	if count_list[key] >= 5:
		dict_list.append(key)
final_dictionary = set(dict_list) # & word_list?

# 3. if minimum distance > 0, correct it with the one that has the minimum distance with it and 
# the minimum distance should be less than 4(or 5, depends)
for key in not_blank_tokens:
	for i in range(len(not_blank_tokens[key])):
		word = not_blank_tokens[key][i]
		if count_list[word] < 5: # it might be a misspelled word
			min_dist = min(final_dictionary, key=lambda x:levenshtein(word,x)) 
			# the correction suggestion would be the first word that has the minimum distance with the misspelled word, 
			# which could be wrong!
			t = levenshtein(min_dist, word) 
			if t > 0 and t < 3:
				not_blank_tokens[key][i] = min_dist

# differentiate stylistinitiated and memberinitiated
for key in not_blank_tokens:
	if stylist[key] == "1":
		stylistinitiated[key] = [word.lower() for word in not_blank_tokens[key]]
	else:
		member[key] = not_blank_tokens[key]

tasktitle_result["stylist initiated"] = stylistinitiated

withcap = [] # a list of taskid of which the tasktitle has capital letters in it
for key in member:
	if any(c.isupper() for c in temp[key]):
		withcap.append(key)		
		
for key in member:
	if key in withcap:
		featuredcollections[key] = temp[key]
	else:
		csc[key] = member[key]

csc_fre_count_sorted = sorted(dict_list_freq_count(csc).items(), key=lambda x: (x[1],x[0]), reverse = True)
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'w') as file:
	for i in range(len(csc_fre_count_sorted)):
		file.write(csc_fre_count_sorted[i][0] + '\t' + str(csc_fre_count_sorted[i][1]) + '\n')

# create a list of comma separated categories
# I want to use this list to determine whether a tasktitle is in old trunk request system or not
csc_list = []
# threshold: frequency > 500
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'r') as file:
	for line in file:
		if int(line.split('\t')[1]) > 500:
			csc_list.append(line.split('\t')[0])
		else:
			break
# manually fix:
csc_list.append("casual")
csc_list.append("dress")
csc_list.append("shirts")
csc_list.append("shirt")
csc_list.append("shoes")
csc_list.append("shoe")
csc_list.append("pants")
csc_list.append("pant")
csc_list.append("jean")
csc_list.append("belt")
csc_list.append("tee")
csc_list.append("blazer")
csc_list.append("polo")
csc_list.append("chino")
csc_list.append("sweater")
csc_list.append("tie")
csc_list.append("bag")		

# principle: after tokenization, if there exists a word in the csc_list, then the task is from the old trunk request system
csc_final = {}
for key in csc:
	if any(word in csc_list for word in csc[key]):
		csc_final[key] = csc[key]
	else:
		others[key] = csc[key]

punct = string.punctuation.translate(None,"_")
fc_tokens = tokenization(featuredcollections,punct)

drop = []
# If featuredcollections is not null, then convert tasktitle to "Featured Collections" no matter what other info it has
for key in featuredcollections:
	if len(fc_id[key]) > 1:
		featuredcollections[key] = "Featured Collections"
	if any(word in csc_list for word in fc_tokens[key]):
		csc_final[key] = [word.lower() for word in fc_tokens[key]]
		drop.append(key)

featuredcollections = {}
for key in member:
	if key in withcap and key not in drop:
		featuredcollections[key] = temp[key]
for key in featuredcollections:
	if len(fc_id[key]) > 1:
		featuredcollections[key] = "Featured Collections"
fc_tokens = tokenization(featuredcollections,punct)

# do frequency count and put those tasktitles appear less than 10 times into others
fc_fre_count = dict_frequency_count(featuredcollections)
fc_fre_count_sorted = sorted(fc_fre_count.items(), key=lambda x: (x[1],x[0]), reverse = True)
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\featured collections frequency count.txt",'w') as file:
	for i in range(len(fc_fre_count_sorted)):
		file.write(fc_fre_count_sorted[i][0] + '\t' + str(fc_fre_count_sorted[i][1]) + '\n')

other_list = ["pack","packed","preview","follow","email","emailed","send","request","call","cc","read",
	"see","need","shipping","address","look","how","what"]

drop = []
for key in featuredcollections:
	if len(fc_id[key]) <= 1:
		if any(word.lower() in other_list for word in fc_tokens[key]):
			drop.append(key)
			others[key] = [word.lower() for word in fc_tokens[key]]			

fc_final = {}
for key in featuredcollections:
	if key not in drop:
		fc_final[key] = featuredcollections[key]

tasktitle_result["featured collections"] = fc_final
tasktitle_result["old trunk request system"] = csc_final
tasktitle_result["others"] = others

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\tasktitle final.csv",'w') as file:
	file.write("taskid" + '\t' + "clean tasktitle" + '\t' + "category" + '\n')
	for key in tasktitle_result:
		if key == "featured collections":
			for key2 in tasktitle_result[key]:
				file.write(key2 + '\t' + str(tasktitle_result[key][key2]) + '\t' + key + '\n')
		else:
			for key2 in tasktitle_result[key]:
				file.write(key2 + '\t' + ','.join(tasktitle_result[key][key2]).lower() + '\t' + key + '\n')

"""
for key in tasktitle:
	if stylist[key] == "1":
		stylistinitiated[key] = tasktitle[key]
	elif tasktitle[key] == "":
		blank[key] = tasktitle[key]
	else:
		member[key] = tasktitle[key]
	# elif re.search(r"^[a-z]",tasktitle[key]) is not None:
		# csc[key] = tasktitle[key]
	# else:
		# featuredcollections[key] = tasktitle[key]

# I haven't populated others now because I need to find a way to detect them.

#### Test ####
# Need to check if the tasktitles in csc and featuredcollections are what we want
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\comma separated categories.txt",'w') as file:
	# for key in csc:
		# file.write(key + '\t' + str(csc[key]) + '\n')
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\featured collections.txt",'w') as file:
	# for key in featuredcollections:
		# file.write(key + '\t' + str(featuredcollections[key]) + '\n')
#### End of Test ####

# There are tasktitles like "starter trunk / The Six Essentials" and "a Business Travel Trunk" in csc. So the above method, which finds
# all tasktitles starting with a non-capital letter and populate them in csc, is not correct. Now fix it.
withcap = [] # a list of taskid of which the tasktitle has capital letters in it
# nocap = [] # a list of taskid of which the tasktitle has no capital letters

for key in member:
	if any(c.isupper() for c in member[key]):
		withcap.append(key)
	# else:
		# nocap.append(key)
# Now repopulate csc and featuredcollections:
for key in member:
	if key in withcap:
		featuredcollections[key] = member[key]
	else:
		csc[key] = member[key]

# rewrite "1st" to "first", "2nd" to "second", "6" to "Six"
for key in featuredcollections:
	featuredcollections[key] = re.sub(r"\b1st\b","first",featuredcollections[key])
	featuredcollections[key] = re.sub(r"\b2nd\b","second",featuredcollections[key])
	featuredcollections[key] = re.sub(r"\b6\b","Six",featuredcollections[key])

# If featuredcollections is not null, then convert tasktitle to "Featured Collections" no matter what other info it has
for key in featuredcollections:
	if len(fc_id[key]) > 1:
		featuredcollections[key] = "Featured Collections"

#### Test ####
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\comma separated categories.txt",'w') as file:
	# for key in csc:
		# file.write(key + '\t' + str(csc[key]) + '\n')
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\featured collections.txt",'w') as file:
	# for key in featuredcollections:
		# file.write(key + '\t' + str(featuredcollections[key]) + '\n')
#### End of Test ####

# There are "others" like "pack trunk - reponse -casual_pants, casual_shirts, polos" in both categories, so we need to differentiate those.
# do frequency count
# for featured collections:
fc_fre_count = dict_frequency_count(featuredcollections)
fc_fre_count_sorted = sorted(fc_fre_count.items(), key=lambda x: (x[1],x[0]), reverse = True)
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\featured collections frequency count.txt",'w') as file:
	for i in range(len(fc_fre_count_sorted)):
		file.write(fc_fre_count_sorted[i][0] + '\t' + str(fc_fre_count_sorted[i][1]) + '\n')

# for csc:
# csc_fre_count = dict_frequency_count(csc)
# csc_fre_count_sorted = sorted(csc_fre_count.items(), key=lambda x: (x[1],x[0]), reverse = True)
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'w') as file:
	# for i in range(len(csc_fre_count_sorted)):
		# file.write(csc_fre_count_sorted[i][0] + '\t' + str(csc_fre_count_sorted[i][1]) + '\n')

# first tokenize csc and then do frequency count of each word
punct = string.punctuation.translate(None,"_")
csc_tokens = tokenization(csc,punct)
csc_tokens_fre_count = dict_list_freq_count(csc_tokens)
csc_fre_count_sorted = sorted(csc_tokens_fre_count.items(), key=lambda x: (x[1],x[0]), reverse = True)
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'w') as file:
	for i in range(len(csc_fre_count_sorted)):
		file.write(csc_fre_count_sorted[i][0] + '\t' + str(csc_fre_count_sorted[i][1]) + '\n')

# create a list of comma separated categories
# I want to use this list to determine whether a tasktitle is in old trunk request system or not
csc_list = []
# threshold: frequency > 500
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'r') as file:
	for line in file:
		if int(line.split('\t')[1]) > 500:
			csc_list.append(line.split('\t')[0])
		else:
			break
# manually fix:
csc_list.append("casual")
csc_list.append("dress")
csc_list.append("shirts")
csc_list.append("shirt")
csc_list.append("shoes")
csc_list.append("shoe")
csc_list.append("pants")
csc_list.append("pant")
csc_list.append("jean")
csc_list.append("belt")
csc_list.append("tee")
csc_list.append("blazer")
csc_list.append("polo")
csc_list.append("chino")
csc_list.append("sweater")
csc_list.append("tie")
csc_list.append("bag")

# principle: after tokenization, if there exists a word in the csc_list, then the task is from the old trunk request system
# csc_final = {}
csc_final_tokens = {}
for key in csc_tokens:
	if any(word in csc_list for word in csc_tokens[key]):
		# csc_final[key] = csc[key]
		csc_final_tokens[key] = csc_tokens[key]
	else:
		others[key] = csc_tokens[key]

# add those comma separated categories in featuredcollections to csc_final
punct = string.punctuation.translate(None,"_")
fc_tokens = tokenization(featuredcollections,punct)
temp = []
csc_final = {}

for key in fc_fre_count:
	if fc_fre_count[key] < 10:
		temp.append(key)

fc_drop = []
for key in fc_tokens:
	if featuredcollections[key] in temp:
		if any(word.lower() in csc_list for word in fc_tokens[key]):
			fc_drop.append(key)
			csc_final[key] = [[],[]]
			for word in fc_tokens[key]:
				if word.lower() in csc_list:
					csc_final[key][0].append(word.lower())
				else:
					csc_final[key][1].append(word.lower())

#### Test ####
# csc_final_fre_count = dict_frequency_count(csc_final)
# csc_fre_count_sorted = sorted(csc_final_fre_count.items(), key=lambda x: (x[1],x[0]), reverse = True)
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc frequency count.txt",'w') as file:
	# for i in range(len(csc_fre_count_sorted)):
		# file.write(csc_fre_count_sorted[i][0] + '\t' + str(csc_fre_count_sorted[i][1]) + '\n')
#### End of Test ####

for key in csc_final_tokens:
	csc_final[key] = [[],[]]
	for word in csc_final_tokens[key]:
		if word in csc_list:
			csc_final[key][0].append(word.lower())
		else:
			csc_final[key][1].append(word.lower())
	if csc_final[key][1] == []:
		csc_final[key][1].append("Null")

#### Test ####
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc final.txt",'w') as file:
	# file.write("taskid" + '\t' + "split tasktitle" + '\t' + "other information" + '\n')
	# for key in csc_final:
		# file.write(key + '\t' + str(csc_final[key][0]) + '\t' + str(csc_final[key][1]) + '\n')
#### End of Test ####

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\csc final.txt",'w') as file:
    file.write("taskid" + '\t' + "split tasktitle" + '\t' + "other information" + '\n')
    for key in csc_final:
		file.write(key + '\t' + ",".join(csc_final[key][0]) + '\t' + ",".join(csc_final[key][1]) + '\n')

temp = []
for key in fc_fre_count:
	if fc_fre_count[key] < 10:
		temp.append(key)

other_list = ["pack","packed","trunk","preview","follow","first","second","email","emailed","send","request","call","cc","read",
	"see","need","shipping","address","look","how","what"]

# tokenize featuredcollections
punct = string.punctuation.translate(None,"_")
fc_tokens = tokenization(featuredcollections,punct)

for key in featuredcollections:
	if len(fc_id[key]) <= 1:
		if featuredcollections[key] in temp:
			if any(word.lower() in other_list for word in fc_tokens[key]):
				fc_drop.append(key)
				others[key] = [word.lower() for word in fc_tokens[key]]

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\fc final.txt",'w') as file:
    file.write("taskid" + '\t' + "featured collections" + '\n')
    for key in featuredcollections:
		if key not in fc_drop:
			file.write(key + '\t' + str(featuredcollections[key]) + '\n')

# We don't need to do anything for blank
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\blank final.txt",'w') as file:
    file.write("taskid" + '\t' + "blank tasktitle" + '\n')
    for key in blank:
		file.write(key + '\t' + str(blank[key]) + '\n')

# for stylist initiated request:
# 1. word tokenization: translate all punctuations except underscore and single quote into blank to split words from stylistinitiated
punct = string.punctuation.translate(None,"_'") # None means only delete underscore and single quotation mark from string.punctuation
drop = ["_","'"]
stylist_tokens = tokenization(stylistinitiated,punct,drop)
#### Test ####
# d = collections.OrderedDict(stylist_tokens)
# x = itertools.islice(d.items(), 0, 10)
# for key, value in x:
    # print key, value
#### End of Test ####

# 2. output all the tasktitles having words that are not in the dictionary of English words to see if there are any abbreviations
# that need to be corrected first(the following file "not in the dictionary.txt" can be used to check the contexts when not sure what the abbreviations mean)
abbr = []
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\not in the dictionary.txt",'w') as file:
	for key in stylist_tokens:
		temp = [tasktitle[key]]
		for word in stylist_tokens[key]:
			if word not in word_list:
				if word.isdigit() == False and len(word) <= 3:
					abbr.append(word)
					temp.append(word)
		if len(temp) > 1:
			file.write(key + '\t' + str(temp) + '\n')

# do frequency count to rewrite the top 10 abbreviations to their full names
abbr_count = sorted(list_frequency_count(abbr).items(), key=lambda x: (x[1],x[0]), reverse = True) # descending order; this is a tuple
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\abbreviations_count.txt",'w') as file:
	for i in range(len(abbr_count)):
		file.write(abbr_count[i][0] + '\t' + str(abbr_count[i][1]) + '\n')

# use regular expression to match the most common abbreviations, modify them as full names and then retokenization
for key in stylistinitiated:
	stylistinitiated[key] = re.sub(r"\bf[\/.]?u[.p]?\b","follow up",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bf[.]?u[.]?t\b","follow up trunk",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bupt\b","up trunk",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bfollowup\b","follow up",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\b1st\b","first",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\b2nd\b","second",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\b3rd\b","third",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\b4th\b","fourth",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bca\b","california",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bny[c]?\b","new york",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bdc\b","washington_dc",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bmp\b","my pleasure",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bdl\b","dl1961",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bw[\/]?\b","with",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\btp\b","top",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bt[\ \-]?shi\b","teeshi",stylistinitiated[key])
	stylistinitiated[key] = re.sub(r"\bt\'s\b","tees",stylistinitiated[key])

stylist_resplit = tokenization(stylistinitiated,punct,drop)

for key in others:
	tasktitle[key] = re.sub(r"\bf[\/.]?u[.p]?\b","follow up",tasktitle[key])
	tasktitle[key] = re.sub(r"\bf[.]?u[.]?t\b","follow up trunk",tasktitle[key])
	tasktitle[key] = re.sub(r"\bupt\b","up trunk",tasktitle[key])
	tasktitle[key] = re.sub(r"\b1st\b","first",tasktitle[key])
	tasktitle[key] = re.sub(r"\b2nd\b","second",tasktitle[key])
	tasktitle[key] = re.sub(r"\b3rd\b","third",tasktitle[key])
	tasktitle[key] = re.sub(r"\b4th\b","fourth",tasktitle[key])
	tasktitle[key] = re.sub(r"\bca\b","california",tasktitle[key])
	tasktitle[key] = re.sub(r"\bny[c]?\b","new york",tasktitle[key])
	tasktitle[key] = re.sub(r"\bdc\b","washington_dc",tasktitle[key])
	tasktitle[key] = re.sub(r"\bmp\b","my pleasure",tasktitle[key])
	tasktitle[key] = re.sub(r"\bdl\b","dl1961",tasktitle[key])
	tasktitle[key] = re.sub(r"\bw[\/]?\b","with",tasktitle[key])
	tasktitle[key] = re.sub(r"\btp\b","top",tasktitle[key])
	tasktitle[key] = re.sub(r"\bt[\ \-]?shi\b","teeshi",tasktitle[key])
	tasktitle[key] = re.sub(r"\bt\'s\b","tees",tasktitle[key])

for key in others:
	others[key] = tasktitle[key]
others_tokens = tokenization(others,punct,drop)
#### Test ####
# abbr = []
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\not in the dictionary.txt",'w') as file:
	# for key in stylistinitiated:
		# temp = [stylistinitiated[key]]
		# for word in stylist_resplit[key]:
			# if word not in word_list:
				# if word.isdigit() == False and len(word) <= 3:
					# abbr.append(word)
					# temp.append(word)
		# if len(temp) > 1:
			# file.write(key + '\t' + str(temp) + '\n')
# abbr_count = sorted(frequency_count(abbr).items(), key=lambda x: (x[1],x[0]), reverse = True) # descending order; this is a tuple
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\abbreviations_count.txt",'w') as file:
	# for i in range(len(abbr_count)):
		# file.write(abbr_count[i][0] + '\t' + str(abbr_count[i][1]) + '\n')
#### End of Test ####

# 3. remove stopwords(strategy: if the word is in the list of stop-words, remove it)
# first check the stop word list
stop_words = get_stop_words('english')
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\stop words.txt",'w') as file:
	# for i in range(len(stop_words)):
		# file.write(str(stop_words[i]) + '\n')
stop_words = [] # I read it again because I don't know how to encode and decode the unicode strings in the original stop_words
with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\stop words.txt",'r') as file:
	for line in file:
		stop_words.append(line.rstrip())

for key in stylist_resplit:
	for word in stop_words:
		while word in stylist_resplit[key]:
			stylist_resplit[key].remove(word)

for key in others_tokens:
	for word in stop_words:
		while word in others_tokens[key]:
			others_tokens[key].remove(word)
#### Test ####
# should print nothing
# for key in stylist_resplit:
	# for word in stylist_resplit[key]:
		# if word in stop_words:
			# print key, word
#### End of Test ####


# use levenshtein distance to correct misspelled words
# 1. do frequency count to generate a dictionary
count_list1 = dict_list_freq_count(stylist_resplit)
count_list2 = dict_list_freq_count(others_tokens)
# with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\frequency_count.txt",'w') as file:
	# for key in count_list:
		# file.write(key + '\t' + str(count_list[key]) + '\n')

# 2. calculate levenshtein distances for each word in each list in the whole dictionary stylist_resplit
# quoted from wikibooks, 5th version, using numpy
def levenshtein(source, target):
	if len(source) < len(target):
		return levenshtein(target, source)
	
	# So now we have len(source) >= len(target).
	if len(target) == 0:
		return len(source)
	
	# We call tuple() to force strings to be used as sequences
	# ('c', 'a', 't', 's') - numpy uses them as values by default.
	source = np.array(tuple(source))
	target = np.array(tuple(target))
	
	# We use a dynamic programming algorithm, but with the added optimization that 
	# we only need the last two rows of the matrix.
	previous_row = np.arange(target.size + 1)
	for s in source:
		# Insertion (target grows longer than source):
		current_row = previous_row + 1
		
		# Substitution or matching:
		# Target and source items are aligned, and either
		# are different (cost of 1), or are the same (cost of 0).
		current_row[1:] = np.minimum(
				current_row[1:],
				np.add(previous_row[:-1], target != s))
		
		# Deletion (target grows shorter than source):
		current_row[1:] = np.minimum(
				current_row[1:],
				current_row[0:-1] + 1)
		
		previous_row = current_row
	
	return previous_row[-1]

# create our dictionary for comparison
dict_list = []
for key in count_list1:
	if count_list1[key] >= 5:
		dict_list.append(key)
for key in count_list2:
	if count_list2[key] >= 5:
		dict_list.append(key)
final_dictionary = set(dict_list) # & word_list

# 3. if minimum distance > 0, correct it with the one that has the minimum distance with it and 
# the minimum distance should be less than 4(or 5, depends)
for key in stylist_resplit:
	for i in range(len(stylist_resplit[key])):
		word = stylist_resplit[key][i]
		if count_list1[word] < 5: # it might be a misspelled word
			min_dist = min(final_dictionary, key=lambda x:levenshtein(word,x)) 
			# the correction suggestion would be the first word that has the minimum distance with the misspelled word, which could be wrong!
			if levenshtein(min_dist, word) > 0 and levenshtein(min_dist, word) < 4:
				stylist_resplit[key][i] = min_dist

for key in others_tokens:
	for i in range(len(others_tokens[key])):
		word = others_tokens[key][i]
		if count_list2[word] < 5: # it might be a misspelled word
			min_dist = min(final_dictionary, key=lambda x:levenshtein(word,x))
			# the correction suggestion would be the first word that has the minimum distance with the misspelled word, which could be wrong!
			if levenshtein(min_dist, word) > 0 and levenshtein(min_dist, word) < 4:
				others_tokens[key][i] = min_dist

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\stylist final.txt",'w') as file:
	for key in stylist_resplit:
		file.write(key + '\t' + ' '.join(stylist_resplit[key]).lower() + '\n')

with open("C:\\Users\\mjin\\Desktop\\TrunkClub_Mengshan\\others final.txt",'w') as file:
	for key in others_tokens:
		file.write(key + '\t' + ' '.join(others_tokens[key]).lower() + '\n')
"""