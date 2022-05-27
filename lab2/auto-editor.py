from textrank4zh import TextRank4Sentence
import json
import numpy as np
import os

def find_lcs_len(s1, s2):  
    m = [ [ 0 for x in s2 ] for y in s1 ]  
    for p1 in range(len(s1)):  
        for p2 in range(len(s2)):  
            if s1[p1] == s2[p2]:  
                if p1 == 0 or p2 == 0:  
                    m[p1][p2] = 1 
                else:  
                    m[p1][p2] = m[p1-1][p2-1]+1 
            elif m[p1-1][p2] < m[p1][p2-1]:  
                m[p1][p2] = m[p1][p2-1]  
            else:               # m[p1][p2-1] < m[p1-1][p2]  
                m[p1][p2] = m[p1-1][p2]  
    return m[-1][-1] 

def addin(intervals, input, output):
    s = " ".join(["{}sec,{}sec".format(i[0], i[1]) for i in intervals]) 
    os.system("auto-editor {} --edit all --add-in {} -o {}".format(input, s, output))

with open('split09.json', encoding='utf-8') as f:
    j = json.load(f)

j = [i for i in j if len(i["onebest"]) > 4]

inters = [[ int(i['bg'])/1000, (int(i['ed'])) / 1000 ] for i in j]
sentences = [i["onebest"] for i in j]
#print(paper)

tr4s = TextRank4Sentence()
tr4s.analyze(text="".join(sentences), lower=True, source = 'all_filters')

print()
print( '摘要：' )
idxs = []
sets = []
for item in tr4s.get_key_sentences(num=3):
    idxs.append(item.index)
    sets.append(item.sentence)
idx = np.argsort(idxs)
sets = np.array(sets)[idx]


for i, s in enumerate(sets):
    targets = []
    for ss, inter in zip(sentences, inters):
        if find_lcs_len(ss, s) > 0.8 * len(ss):
            targets.append(inter)

    addin(targets, "split09.mp4", "{}.mp4".format(i))

# summarize = jiagu.summarize(paper, 5) # 摘要
# print( '摘要：' )
# print(summarize)

# summ = summarize(paper, 5)
# print( '摘要：' )
# print(summ)
# import macropodus

# 文本摘要(summarize, 默认接口)
# sents = macropodus.summarize(paper)
# print(sents)

# 文本摘要(summarization, 可定义方法, 提供9种文本摘要方法, text_pronouns, text_teaser, word_sign, textrank, lead3, mmr, lda, lsi, nmf)
# for alg in ['text_pronouns', 'text_teaser', 'word_sign', 'textrank', 'lead3', 'mmr', 'lda', 'lsi', 'nmf']:
#     sents = macropodus.summarization(text=sentences, type_summarize=alg)
#     idxs = np.array([sen[0] for sen in sents])
#     sent = np.array([sen[1] for sen in sents])
#     idx = np.argsort(-idxs)
#     sent  = sent[idx]
#     print(alg)
#     print(sent[:3])
#print(idxs[idx])