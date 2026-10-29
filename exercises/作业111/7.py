word='The quick brown fox jumps over the lazy dog. The dog wakes up and runs after the fox. The fox is too quick, and the lazy dog cannot catch it. Python is a powerful programming language. It is easy to learn and fun to use. Learning Python can help you build amazing projects quickly.'
words_list = word.lower().replace(",", "").replace(".", "").split()
d1 = list(dict.fromkeys(words_list))
print(d1)
d2 ={}
'''''
for i in words_list:
    if i not in d2:
        d2[i] = 1
    else:
        d2[i] +=1
print(sorted(d2.items(),key=lambda x:x[1],reverse=True)[:3])
'''''
for w in words_list:
    d2[w] = d2.get(w, 0) + 1
print(d2)