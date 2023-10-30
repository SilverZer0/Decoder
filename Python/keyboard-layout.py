qwerty  = r'''`1234567890-=~!@#$%^&*()_+qwertyuiop[]\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?'''
dovorak = r'''`1234567890[]~!@#$%^&*(){}',.pyfgcrl/=\"<>PYFGCRL?+|aoeuidhtns-AOEUIDHTNS_;qjkxbmwvz:QJKXBMWVZ'''
workman = r'''`1234567890-=~!@#$%^&*()_+qdrwbjfup;[]\QDRWBJFUP:{}|ashtgyneoi'ASHTGYNEOI"zxmcvkl,./ZXMCVKL<>?'''

def o(L):
    return [ord(i) for i in L]

ALL = {'qwerty ':o( qwerty),
       'dovokak':o(dovorak),
       'workman':o(workman)}

IN = input('text: ')
for i_n, i_k in ALL.items():
    for j_n, j_k in ALL.items():
        if i_n == j_n:
            continue
        print(f'{i_n} -> {j_n}:\t',IN.translate({i_k[x]:j_k[x] for x in range(91)}))
