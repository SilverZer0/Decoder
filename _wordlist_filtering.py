import pandas as pd
import os
import csv

#https://wortschatz.uni-leipzig.de/en/download/English

PATH = r'C:\Users\j\Downloads\wordlists'
kwargs = {'sep':'\t', 'quoting':csv.QUOTE_NONE, 'header':None, 'keep_default_na':False}
eng = []
for i in os.listdir(PATH):
    if i.startswith('eng'):
        eng.append(pd.read_csv(os.path.join(PATH, i), names=['word', 'count'], index_col=0, **kwargs))
old = pd.read_csv(os.path.join(PATH, 'WordsEng.txt'), names=['word'], index_col=False, **kwargs)

chars = ''.join(sorted(set(''.join(map(str,old.iloc[:,0])))))+' '

def f(s):
    return ''.join(i if i in chars else '?' for i in s)

for i in eng:
    i['word'] = i['word'].apply(f)
    i['word'] = i['word'].str.lower()
    i['word'] = i['word'].str.strip('!&\',-./? ')

new = {}
for d in eng:
    length = len(d)
    for w,c in zip(d['word'], d['count']):
        ws = w
        for i in '!&,-./?':
            ws = ws.replace(i, ' ')
        ws = ws.split(' ')
        for i in ws:
            if not i in new:
                new[i] = [0,0]
            new[i][0] += c/length
            new[i][1] += c

keys = new.keys()
df = pd.DataFrame(zip(keys, [new[i][1] for i in keys], [new[i][0] for i in keys]))
df.columns = ['word', 'count', 'count_pro']
df.sort_values(['count'], ascending=False, inplace=True)
df.reindex()

cut = df[(df['count'] > 1) | pd.Series([i in old for i in df['word']])]
cut['word'].to_csv(os.path.join('WordsEng_2.txt'), index=False, header=False)
