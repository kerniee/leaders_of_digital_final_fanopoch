import math
import json
import string

from simple_elmo import ElmoModel

model = ElmoModel()

model.load("199")
#not_specified_string="не указано"
#not_specified_string_in="неуказано"

key_vectors = []

key_lengths = []
key_words = []
keys = []
keys_grouped = []

def calculate_keys(keysIn):
    global key_vectors, key_words, key_lengths, keys_grouped, keys
    keys_grouped = keysIn
    for key_group in keys_grouped:
        #key_group.append(not_specified_string)
        for key in key_group:
            keys.append(key)
            key_words.append(sentence_to_words(key))
            key_lengths.append(len(key_words[len(key_words) - 1]))
    key_vectors = []
    #key_vectors_pre=model.get_elmo_vectors_shit(key_words, layers="average")
    #for key in key_vectors_pre:
    #    key_vectors.append(sum(key))
    for t in key_words:
        key_vectors.append(sum(model.get_elmo_vectors([t], layers="average")[0]))
    with open("key_vectors.json", "w") as outfile:
        outfile.write(
        json.dumps(key_vectors))

def load_keys(keys_in, filename):
    global key_vectors, key_words, key_lengths, keys_grouped, keys
    keys_grouped = keys_in
    for key_group in keys_grouped:
        #key_group.append(not_specified_string)
        for key in key_group:
            keys.append(key)
            key_words.append(sentence_to_words(key))
            key_lengths.append(len(key_words[len(key_words) - 1]))
    with open(filename, "r") as infile:
        key_vectors = json.load(infile)

def sentence_to_words(sentenceI):
    sentence = sentenceI
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    sentence = sentence.split()
    return sentence


def dist(a, b):
    dsq = 0
    for i in range(len(a)):
        dsq += abs(a[i] - b[i]) ** 2
    return math.sqrt(dsq)

def sum(key_check):
    v = [0] * len(key_check[0])
    for t in key_check:
        for i in range(0, len(t)):
            v[i] = v[i] + (t[i]/ (len(key_check)/1.5))
    return v

def avg(key_check):
    v = [0] * len(key_check[0])
    for t in key_check:
        for i in range(0, len(t)):
            v[i] = v[i] + (t[i] / len(key_check))
    return v


def keys_check(sentenceI):
    global keys, key_lengths, key_words, key_vectors,keys_grouped
    sentence=sentenceI.lower()+" "#+not_specified_string_in
    scores = []
    sentence_vectors = []

    sentence_vectors = model.get_elmo_vectors([sentence_to_words(sentence)], layers="average")[0]

    # print()

    temp_val = ""
    temp_key = ""
    for i in range(0, len(key_vectors)):
        temp_scores = 99999999999999
        for j in range(0, len(sentence_vectors) - key_lengths[i]):
            key_check = []
            origin_check = []
            for k in range(0, key_lengths[i]):
                key_check.append(sentence_vectors[j + k])
                origin_check.append(sentence_to_words(sentence)[j + k])
            key_check_average = sum(key_check)
            ts = dist(key_vectors[i], key_check_average)
            if ts < temp_scores:
                temp_scores = ts
                temp_val = origin_check
        scores.append(temp_scores)
        #print("FINAL!")
        #print(keys[i])
        #print(temp_val)
        #print(temp_scores)
        #print()
    return scores


def keys_grouped_check(sentence):
    scores=keys_check(sentence)
    iterator=0
    scores_grouped=[]
    keys_selected=[]
    for key_group in keys_grouped:
        key_selected=""
        key_best_match=999999999999
        scores_grouped.append([])
        for key in key_group:
            cur_score=scores[iterator]
            if cur_score<key_best_match:
                key_best_match=cur_score
                key_selected=key
            scores_grouped[len(scores_grouped)-1].append(cur_score)
            iterator+=1
        keys_selected.append(key_selected)
    return keys_selected