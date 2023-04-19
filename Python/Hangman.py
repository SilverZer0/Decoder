def Filter():
    #Hangman
    List = []
    Guess = 'et'
    Word = 'alar_'
    contains = ''
    Guess = ''.join(i for i in Guess if not i in contains)+''.join(i for i in Word if not i == '_')
    for i in Words:
        if len(i) == len(Word) and all([Word[j] in (i[j],'_') for j in range(len(i))])\
           and all([not i[j] in Guess for j in range(len(i)) if Word[j] == '_']):
            List.append(i)
    D = {}
    List = [i for i in List if all(j in i for j in contains)]
    for i in List:
        for j in range(len(Word)):
            if Word[j] == '_':
                if not i[j] in D:
                    D[i[j]] = 1
                else:
                    D[i[j]] += 1
    List2 = sorted([(i,D[i]) for i in D],key=lambda x:-x[1])
    return List,List2
    
#import re to make it easier
file = open('wordsEng.txt', 'r')
Words = []
for line in file:
    Words.append(line[0:-1].lower())
file.close()
List,List2 = Filter()
if len(List) <= 10:
    print(f'{List = }')
else:
    print(f'{len(List) = }')
print(f'{List2 = }')
