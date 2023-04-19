import re

with open('wordsEng.txt','r') as file:
    Words = file.read().split('\n')

def run(IN=None):
    if IN is None:
        IN = input('Please enter encrypted Text: ')
        try:
            IN = eval(IN)
        except Exception:
            pass
        commands('')
        Code = input('\nYour Choice: ').upper()
    else:
        Code = input('\nCommands at the Beginning\nYour Choice: ').upper()
    #Lists(IN)
    Options = {
        'C':commands,
        'L':language,
        'Py':python,
        'A':Automatic,
        '0':Annagram,
        '1':Ascii,
        '2':Cesar,
        '3':Morse,
        '4':Numbers,
        '5':Pop_nth,
        '6':Base,
        '7':Re_match,
        '8':Vigenere,
        '9':Braille,
        '-':Atbash
        }
    while 1:
        if Code in Options:
            OUT = Options[Code](IN)
            if Code in 'CL':
                Code = input('\nYour Choice: ').upper()
                continue
            IN = end(IN,OUT)
            Code = input('\nCommands at the Beginning\nYour Choice: ').upper()
        else:
            Code = input('Invalid Input. Try again: ').upper()

# is it used/usefull?
def Lists(IN):
    # P1 Overall Probability | P2 Probability to be in a Word
    P1Eng = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm',
             'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
    P2Eng = ['e', 'i', 'a', 'r', 'n', 'o', 's', 't', 'l', 'c', 'u', 'd', 'p', 'm',
             'h', 'g', 'y', 'b', 'f', 'v', 'k', 'w', 'z', 'x', 'q', 'j']

    P1Ger = ['e', 'n', 'i', 's', 'r', 'a', 't', 'd', 'h', 'u', 'l', 'c', 'g', 'm',
             'o', 'b', 'w', 'f', 'k', 'z', 'p', 'v', 'ü', 'ä', 'ö', 'ß', 'j', 'y',
             'x', 'q']
    P2Ger = ['e', 'n', 'r', 's', 't', 'i', 'a', 'l', 'u', 'h', 'g', 'c', 'o', 'd',
             'm', 'b', 'k', 'f', 'p', 'z', 'w', 'ä', 'v', 'ü', 'ö', 'y', 'ß', 'x',
             'j', 'q']
    global Content
    global Count
    global Ranking
    global Portion
    Content = []
    Count = []
    Ranking = []
    Portion = []
    for i in range(len(IN)):
        if not IN[i] in Content:
            Content.append(IN[i])
            Count.append(0)
    Content.sort()
    for i in range(len(IN)):
        Count[Content.index(IN[i])] += 1
    for i in range(len(Count)):
        Portion.append(Count[i] / len(IN))
        Ranking.insert(0, Content[i])
        for j in range(len(Ranking) - 1):
            if Count[Content.index(Ranking[j])] < Count[Content.index(Ranking[j + 1])]:
                Ranking.insert(j, Ranking.pop(j + 1))
            else:
                break

def end(IN, OUT=''):
    if len(OUT) == 1:
        OUT = OUT[0]
    if isinstance(OUT, list):
        OUT = [str(i) for i in OUT]
        print(f'\nIN: {str(IN)}\nOUT:')
        for i,j in enumerate(OUT):
            print(f'{i}: {j}')
        print(f"{len(OUT)}: {' '.join(OUT)}")
    else:
        print(f'\nIN: {str(IN)}\nOUT: {str(OUT)}')
    Code = input('\n0 - End Program\n'
                 + '1 - Use other methode on IN\n'
                 + '2 - Use other methode on OUT'
                 + '\n3 - New Input\nYour Choice: ')
    while 1:
        if Code == '0':
            exit()
        elif Code == '1':
            return IN
        elif Code == '2':
            if isinstance(OUT, list):
                return OUT[int(ask('Which element of OUT should be used? ', f'x.isdecimal() and x < {len(OUT)}'))]
            else:
                return OUT
            break
        elif Code == '3':
            return input('\nPlease new Input: ')
        else:
            Code = input('Invalid Input. Try again: ')

def commands(IN):
    print('\nL - change language\n'
          + 'C - print commands again\n'
          + 'Py- Python environment\n'
          + 'A - Decode automatically\n'
          + '0 - Anagram\n'
          + '1 - Ascii\n'
          + '2 - Cesar\n'
          + '3 - Morse\n'
          + '4 - Numbers(1 to 26)\n'
          + '5 - remove every nth letter\n'
          + '6 - Change base (2 <= base <= 36)\n'
          + '7 - pattern (re)\n'
          + '8 - Vigenere (IN + Key)\n'
          + '9 - Braille (No input)\n')

def ask(s,c):
    c = eval('lambda x: '+c)
    x = input(s)
    while not c(x):
        x = input('Invalid. Try again: ')
    return x

def language(IN):
    global Words
    l = ask('Eng or Ger? ', "x.lower() in ('eng','e','ger','g')")
    if l.lower() in ('eng','e'):
        with open('wordsEng.txt','r') as file:
            Words = file.read().split('\n')
    else:
        with open('wordsGer.txt','r') as file:
            Words = file.read().split('\n')

def python(IN):
    print('input is `IN´; use `break´ to exit')
    OUT = None
    while 1:
        try:
            eval(input('>>> '))
        except Exception as e:
            print('Error:',e)
    if OUT is None:
        return IN
    return OUT

# Make it work
def Automatic(IN):
    print('Not Implemented')
    return ''

# add multi word
def Annagram(IN):
    return [i for i in Words if len(i) == len(IN) and
            sorted(list(IN.lower())) == sorted(list(i.lower()))]

def Ascii(IN):
    In = IN.replace(' ',',').replace(',,',',').split(',')
    if set(IN).issubset(set('1234567890 ,')):
        return [chr(int(i)) for i in In]
    else:
        return [ord(i) for i in In]

def Cesar(IN, Rot=None):
    if Rot is None:
        Rot = int(ask('Rotation? ', 'x.isdecimal()'))%26
    if Rot == 0:
        return [Cesar(IN,Rot=i) for i in range(1,26)]
    else:
        OUT = ''
        for j in IN:
            if ord(j) in range(65,91):
                OUT += chr((ord(j)-65+Rot)%26+65)
            elif ord(j) in range(97,123):
                OUT += chr((ord(j)-97+Rot)%26+97)
            else:
                OUT += j
        return OUT

# not all are showen
def Morse(IN):
    Morse_d = {'01': 'a', '1000': 'b', '1010': 'c', '100': 'd', '0': 'e',
             '0010': 'f', '110': 'g', '0000': 'h', '00': 'i', '0111': 'j',
             '101': 'k', '0100': 'l', '11': 'm', '10': 'n', '111': 'o',
             '0110': 'p', '1101': 'q', '010': 'r', '000': 's', '1': 't',
             '001': 'u', '0001': 'v', '011': 'w', '1001': 'x', '1011': 'y',
             '1100': 'z', '':' ',
             '11111': '0', '01111': '1', '00111': '2', '00011': '3', '00001': '4',
             '00000': '5', '10000': '6', '11000': '7', '11100': '8', '11110': '9'}

    def per(L):
        if len(L) == 0:
            return []
        if len(L) == 1:
            return [L]
        l = []
        for i in range(len(L)):
            m = L[i]
            remLst = L[:i] + L[i+1:]
            for p in per(remLst):
                l.append([m] + p)
        return l

    
    if len(set(IN)) > 4:
        print('\nYour input is unfit for Morse')
        return ''
    
    OUT = []
    for i in per(list(set(IN))):
        valid = True
        r = ''
        In = IN
        if len(set(IN)) == 4:
            for j in (i[2]+i[3]+i[2],i[2]+i[3],i[3]+i[2]):
                In = IN.replace(j,i[2]+i[2])
        In = In.replace(i[0],'Ӓ').replace(i[1],'1').replace('Ӓ','0').split(i[2])
        for j in In:
            try:
                r += Morse_d[j]
            except KeyError:
                valid = False
                break
        if valid:
            OUT.append(r)
    return OUT

def Numbers(IN):
    In = IN.replace(' ',',').replace(',,',',').split(',')
    if set(IN).issubset(set('1234567890 ,')):
        return [chr(int(i)+64) for i in In]
    else:
        return [ord(i.upper())-64 for i in In]

def Pop_nth(IN, Code=None):
    if Code is None:
        Code = ask('n: ','x.isdecimal()')
    OUT = ''
    for i in range(len(IN)):
        if (i + 1) % Code != 0:
            OUT += IN[i]
    return OUT

def Base(IN, In_b=None, Out_b=None):
    if In_b is None or Out_b is None :
        In_b = int(ask('What is the current Base? ','x.isdecimal() and  1 < int(x) < 37'))
        Out_b = int(ask('What is the target Base? ','x.isdecimal() and  1 < int(x) < 37'))
    In = [int(i,In_b) for i in IN.replace(' ',',').replace(',,',',').split(',')]
    Py = {2:bin, 8:oct, 16:hex}
    if Out_b in Py:
        OUT = ' '.join([Py[Out_b](i)[2:] for i in In])
    elif Out_b == 10:
        OUT = ' '.join([str(i) for i in In])
    else:
        nums = (list(str(i) for i in range(10)) + list(chr(i) for i in range(65,91)))[:Out_b]
        OUT = ''
        for i in In:
            r = ''
            while i:
                r = nums[i % Out_b] + r
                i //= Out_b
            OUT += ' ' + r
    return OUT

def Re_match(IN):
    return [i for i in Words if bool(re.match(IN.lower(),i.lower()))]

def Vigenere(IN, Key=None):
    if Key is None:
        Key = ask('Key? ','x.isalpha()')
    Key = [ord(i)-64 for i in Key.upper()*(int(len(IN)/len(Key))+1)]
    OUT = ''
    for i,j in enumerate(IN):
        OUT += chr((ord(j)-64-(32*j.islower())+Key[i])%26+64+(32*j.islower()))
    return OUT

def Braille(IN):
    print('A ⠁\tF ⠋\tK ⠅\tP ⠏\tU ⠥\tZ ⠵\t0 ⠚\t5 ⠑\n'
          + 'B ⠃\tG ⠛\tL ⠇\tQ ⠟\tV ⠧\t  ⠀\t1 ⠁\t6 ⠋\n'
          + 'C ⠉\tH ⠓\tM ⠍\tR ⠗\tW ⠺\t  ⠀\t2 ⠃\t7 ⠛\n'
          + 'D ⠙\tI ⠊\tN ⠝\tS ⠎\tX ⠭\t  ⠀\t3 ⠉\t8 ⠓\n'
          + 'E ⠑\tJ ⠚\tO ⠕\tT ⠞\tY ⠽\t  ⠀\t4 ⠙\t9 ⠊')
    return ''

def Atbash(IN):
    table = {i:155-i for i in range(65,91)}
    table.update({i:219-i for i in range(97,123)})
    return IN.translate(table)


while 1:
    try:
        run()
    except Exception as e:
        print('Error:',e)

#py env as option
