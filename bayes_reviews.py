import re
import string
import nltk
import math

stop_words = set(nltk.corpus.stopwords.words('english'))
from nltk.stem import PorterStemmer
stemmer= PorterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

file = open('train.data', 'r')
word_count = {}
word_count_target={'spam':{}, 'ham':{}}
spam = 0
ham = 0
lines = len(file.readlines())
file.close()
# test = int(lines*0.3)
test_file = open('test.data', 'r')
test = len(test_file.readlines())
print(test)
train = lines
spam_lines = 0
file = open('train.data', 'r')
for _ in range(train):
    line = file.readline().strip().lower()
    if not line:
        continue
    # line = re.sub(r'\d+', '', line)
    line = line.translate(line.maketrans("","",string.punctuation))
    line = line.split()
    target = line.pop()
    # print(target)
    line = set(line)-stop_words
    line = [lemmatizer.lemmatize(stemmer.stem(word)) for word in line]
    if target == '0':
        spam_lines += 1
    for word in line:
        word = word.strip()
        if word in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1
        if target=='0':
            if word in word_count_target['spam'].keys():
                word_count_target['spam'][word] += 1
            else:
                word_count_target['spam'][word] = 1
        else:
            if word in word_count_target['ham'].keys():
                word_count_target['ham'][word] += 1
            else:
                word_count_target['ham'][word] = 1

total_words = sum(word_count.values())
word_prob = {key:value/total_words for key, value in word_count.items()}
# print(word_prob)

total_spam_words = sum(word_count_target['spam'].values())
total_ham_words = total_words-total_spam_words
word_target_prob = {'spam':{key:value/total_spam_words for key, value in word_count_target['spam'].items()}, \
                        'ham':{key:value/total_ham_words for key,value in word_count_target['ham'].items()}}

distinct_spam_words = len(word_count_target['spam'].keys())
distinct_ham_words = len(word_count_target['ham'].keys())
stat_spam_prob = spam_lines/lines
stat_ham_prob = 1-stat_spam_prob

pos_reviews = 0
true_positive = 0
false_positive = 0
false_negative = 0
true_negative = 0   
correct = 0
test_file = open('test.data', 'r')
for _ in range(test):
    line = test_file.readline().strip().lower()
    if not line:
        continue
    # line = re.sub(r'\d+', '', line)
    line = line.translate(line.maketrans("","",string.punctuation))
    line = line.split()
    target = line.pop()
    if target == '1':
        pos_reviews+=1
    line = set(line)-stop_words
    line = [lemmatizer.lemmatize(stemmer.stem(word)) for word in line]
    ham_prob = stat_ham_prob
    spam_prob = stat_spam_prob
    s_words = distinct_spam_words
    h_words = distinct_ham_words
    for word in line:
        if word not in word_target_prob['spam'].keys():
            s_words += 1
        if word not in word_target_prob['ham'].keys():
            h_words += 1
    for word in line:
        word = word.strip()
        if word in word_target_prob['spam'].keys():
            spam_prob *= word_target_prob['spam'][word] 
        else:
            spam_prob *= (1/s_words)
        if word in word_target_prob['ham'].keys():
            ham_prob *= word_target_prob['ham'][word]
        else:
            ham_prob *= (1/h_words)

        # if word in word_target_prob['spam'].keys():
        #     spam_prob += -math.log(word_target_prob['spam'][word]) 
        # else:
        #     spam_prob += -math.log(1/s_words)
        # if word in word_target_prob['ham'].keys():
        #     ham_prob += -math.log(word_target_prob['ham'][word])
        # else:
        #     ham_prob += -math.log(1/h_words)
    if (spam_prob>ham_prob):
        if target == '0':
            true_negative+=1
            correct += 1
        else:
            false_positive+=1
    elif target == '1':
        true_positive+=1
        correct += 1
    else:
        false_negative+=1
precision = true_positive/(true_positive+false_positive)
recall = true_positive/(true_positive+false_negative)
f1_score = (2*precision*recall)/(precision+recall)
print("Accuracy: ", correct*100/test)
print("Precision: ", precision)
print("Recall: ", recall)
print("f1_scroe: ", f1_score)
