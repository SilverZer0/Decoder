import tkinter as tk
from tkinter import ttk
from re import search as re_search

root = tk.Tk()
root.title('Super-Decoder')
root.geometry('700x790')
root.resizable(False, False)

class Input:
    pass

class Tools:
    def make_tab(self:'Encoding object', name:str, midpad:int=15) -> None:
        ''' makes new standart tab '''
        self.tab = ttk.Frame(tabControl)
        self.tab.pack()
        tabControl.add(self.tab, text=name)
        self.IN = tk.Text(self.tab, height=15)
        self.IN.bind('<KeyRelease>', self.decode)
        self.IN.grid(column=1, row=1, columnspan=12, sticky='N', padx=27, pady=(15,midpad))
        self.OUT = tk.Text(self.tab, height=25, state='disabled')
        self.OUT.grid(column=1, row=3, columnspan=12, sticky='S', padx=27, pady=(midpad,15))

    def make_words_tab(self:'Encoding object', name:str) -> None:
        ''' makes tab with long OUT '''
        self.tab = ttk.Frame(tabControl)
        self.tab.pack()
        tabControl.add(self.tab, text=name)
        def scroll(self, *args, event=None):
            for i in self.OUT:
                if event is None:
                    i.yview(*args)
                else:
                    i.yview_scroll(10 if event.num==5 else -10, 'unit')
            return 'break'
        # .pad to replace IN(pady=)
        self.pad = tk.Label(self.tab, font=('Times 5'))
        self.pad.grid(column=1, row=1, columnspan=12)
        self.IN = tk.Text(self.tab, height=1, width=20)
        self.IN.grid(column=1, row=2, columnspan=3)
        self.IN.bind('<Return>', self.decode)
        self.search = ttk.Button(self.tab, text='Search', command=self.decode)
        self.search.grid(column=3, row=2, columnspan=2)
        self.words = Tools.make_input(self, 5, 'Wordlist:', 'WordsEng', ttk.Combobox, trace=False, width=12,
                                      state='readonly', values=('WordsEng', 'WordsGer', 'OUT_Annagram', 'OUT_Regex'))
        self.scrollbar = ttk.Scrollbar(self.tab, orient='vertical', command=lambda *args:scroll(self, *args))
        self.scrollbar.grid(column=12, row=3, sticky='NS')
        self.OUT = []
        for i in range(4):
            self.OUT.append(tk.Text(self.tab, height=41, width=19, state='disabled', wrap='none', yscrollcommand=self.scrollbar.set))
            print(i,27*(i==0))
            self.OUT[i].grid(column=i*3, row=3, columnspan=3, sticky='S', padx=(27*(i==0),0), pady=15)
            self.OUT[i].bind('<Button-4>', lambda event:scroll(self, event=event))
            self.OUT[i].bind('<Button-5>', lambda event:scroll(self, event=event))
        self._OUT = ''

    def make_input(self:'Encoding object', column:int, label_text:str, default_value:str,
                   input_object:'tk/ttk input Object', trace=True, **input_kwargs) -> object:
        ''' makes input object {label:Label, value:StringVar, input:input_object} '''
        obj = Input()
        obj.label = tk.Label(self.tab, text=label_text)
        obj.label.grid(column=column, row=2, sticky='E')
        obj.value = tk.StringVar()
        obj.value.set(default_value)
        if trace:
            obj.value.trace_add('write', self.decode)
        if input_object == ttk.Checkbutton:
            obj.input = input_object(self.tab, variable=obj.value, **input_kwargs)
        else:
            obj.input = input_object(self.tab, textvariable=obj.value, **input_kwargs)
        obj.input.grid(column=column+1, row=2, sticky='W')
        return obj

    def make_reverse(self:'Encoding object', column:int) -> None:
        ''' makes a reverse CheckButton using Tools.make_input '''
        self.reverse = Tools.make_input(self, column, 'reverse:', 'no', ttk.Checkbutton, onvalue='yes', offvalue='no')
        # .bind() instead of command= because it needs to happen before obj.value.trace_add
        self.reverse.input.bind('<ButtonRelease>', lambda _ : Tools.switch(self))

    def switch(self:'Encoding object') -> None:
        ''' switches IN and OUT (by moving the value of OUT to IN and letting the decoder do the rest)'''
        self.IN.delete('1.0', 'end')
        self.IN.insert('1.0', self.OUT.get('1.0', 'end-1c'))
        self.decode()

    def try_wrap(iterable, func, default='_', constant=(' ','\n',''), special={}):
        for i in iterable:
            if i in constant:
                yield i
                continue
            if i in special:
                yield special[i]
                continue
            try:
                yield func(i)
            except Exception as e:
                yield default

    def write_OUT(func):
        def inner(self, *args, **kwargs):
            Tools.write(self.OUT, func(self, self.IN.get('1.0', 'end-1c')))
        return inner

    def write_words_OUT(func):
        def inner(self, *args, **kwargs):
            if self.words.value.get() == 'WordsEng':
                with open('wordsEng.txt', 'r') as f:
                    self._OUT = func(self, self.IN.get('1.0', 'end-1c'), f.read().split('\n'))
            elif self.words.value.get() == 'WordsGer':
                with open('wordsGer.txt', 'r') as f:
                    self._OUT = func(self, self.IN.get('1.0', 'end-1c'), f.read().split('\n'))
            elif self.words.value.get() == 'OUT_Annagram':
                self._OUT = func(self, self.IN.get('1.0', 'end-1c'), Tabs[0]._OUT)
            else:#OUT_Regex
                self._OUT = func(self, self.IN.get('1.0', 'end-1c'), Tabs[8]._OUT)
            q = (len(self._OUT)//4)+1
            for i in range(4):
                Tools.write(self.OUT[i], '\n'.join(self._OUT[q*i:q*i+q]+['']*(i==3)*(4-len(self._OUT)%4)))
            return 'break'
        return inner

    def write(obj, text):
        obj['state'] = 'normal'
        obj.delete('1.0', 'end')
        obj.insert('1.0', text)
        obj['state'] = 'disabled'        

class Annagram():
    def __init__(self):
        Tools.make_words_tab(self, 'Annagram')
        self.type = Tools.make_input(self, 9, 'type:', 'match', ttk.Combobox, trace=False, width=7,
                                      state='readonly', values=('match', 'bigger', 'smaller'))

    @Tools.write_words_OUT
    def decode(self, IN, Words):
        if self.type.value.get() == 'match':
            return [i for i in Words if len(i) == len(IN) and sorted(IN.lower()) == sorted(i.lower())]
        elif self.type.value.get() == 'bigger':
            return [i for i in Words if len(i) >= len(IN) and self.issublist(IN.lower(), i.lower())]
        else:#smaller
            return [i for i in Words if len(i) <= len(IN) and self.issublist(i.lower(), IN.lower())]

    def issublist(self, a, b):
        b = list(b)
        for i in a:
            if i in b:
                b.remove(i)
            else:
                return False
        return True
        
class Ascii():
    def __init__(self):
        Tools.make_tab(self, '  Ascii ')
        self.type = Tools.make_input(self, 5, 'type:', '1-26 dec', ttk.Combobox, state='readonly', width=8,
                                     values=('1-26 dec', '1-26 bin', '1-26 hex',
                                             'ascii dec', 'ascii bin', 'ascii hex'))
        Tools.make_reverse(self, 7)

    @Tools.write_OUT
    def decode(self, IN):
        func = ['']*5
        form, base = self.type.value.get().split(' ')
        if self.reverse.value.get() == 'yes':
            func[0] = "f'{ord(x)"
            func[4] = "}'"
            if form == '1-26':
                IN = IN.upper()
                func[2] = '-64'
            if base == 'bin':
                func[3] = ':08b'
            elif base == 'hex':
                func[3] = ':02x'
            return ' '.join(Tools.try_wrap(IN, eval('lambda x: '+''.join(func)), constant=('\n',)))
        IN = IN.replace('\n',' \n ').split(' ')
        func[0] = 'chr(int(x'
        func[4] = ')'
        if form == '1-26':
            func[2] = '+64'
        if base == 'dec':
            func[1] = ')'
        elif base == 'bin':
            func[1] = ',2)'
        else:#hex
            func[1] = ',16)'
        return ''.join(Tools.try_wrap(IN, eval('lambda x: '+''.join(func)), constant=('\n',), special={'':' '}))

class Atbash():
    def __init__(self):
        Tools.make_tab(self, 'Atbash', midpad=13)
        self.switch = ttk.Button(self.tab, text='switch', command=lambda: Tools.switch(self))
        self.switch.grid(column=6, row=2, columnspan=2)

    @Tools.write_OUT
    def decode(self, IN):
        table = {i:155-i for i in range(65,91)}
        table.update({i:219-i for i in range(97,123)})
        return IN.translate(table)

class Base():
    def __init__(self):
        Tools.make_tab(self, '  Base ')
        self.IN_base = Tools.make_input(self, 5, 'IN-Base:', '2', ttk.Entry, validate='key', width=5,
                                        validatecommand = (root.register(self.validate), '%P'))
        self.OUT_base = Tools.make_input(self, 7, 'OUT-Base:', '10', ttk.Entry, validate='key', width=5,
                                         validatecommand = (root.register(self.validate), '%P'))

    @Tools.write_OUT
    def decode(self, IN):
        IN_Base = int(self.IN_base.value.get() or '1')
        OUT_Base = int(self.OUT_base.value.get() or '1')
        if IN_Base < 2 or OUT_Base < 2:#when user types 10 the base is 1 for a moment
            return ''
        if IN_Base == OUT_Base:
            return IN
        IN = Tools.try_wrap(IN.replace('\n',' \n ').split(' '), lambda x: int(x, IN_Base))
        Py = {2:"f'{x:b}'", 8:"f'{x:o}'", 16:"f'{x:x}'"}
        if OUT_Base in Py:
            OUT = ' '.join(Tools.try_wrap(IN, lambda x: eval(Py[OUT_Base])))
        elif OUT_Base == 10:
            OUT = ' '.join(f'{i}' for i in IN)
        else:
            nums = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            OUT = ''
            for i in IN:
                if i == '\n':
                    OUT += '\n'
                    continue
                r = ''
                while i:
                    r = nums[i % OUT_Base] + r
                    i //= OUT_Base
                OUT += ' ' + r
        return OUT.replace(' \n ','\n')

    def validate(self, value):
        try:
            return value == '' or 0 <= int(value) <= 36
        except ValueError:
            return False

    def switch(self):
        Tools.switch(self)
        IN_Base = self.IN_base.value.get()
        OUT_Base = self.OUT_base.value.get()
        self.IN_base.value.set(OUT_Base)
        self.OUT_base.value.set(IN_Base)

class Braille():
    def __init__(self):
        Tools.make_tab(self, 'Braille', midpad=5)
        self.char = tk.Text(self.tab, height=1, width=1, state='disabled',
                            bg='grey95', font=('TkFixedFont', 25))
        self.char.grid(column=5, row=2, ipadx=4)
        self.submit_button = ttk.Button(self.tab, text='Submit', command=self.submit)
        self.submit_button.grid(column=6, row=2)
        self.reset_button = ttk.Button(self.tab, text='Reset', command=self.reset)
        self.reset_button.grid(column=7, row=2)
        #self.type = Tools.make_input(self, 7, 'input', '895623', ttk.Combobox, state='readonly', width=6,
        #                             trace=False, values=('895623', '784512'))
        Tools.make_reverse(self, 8)
        self.reverse.input.bind('<ButtonRelease>', self.switch)

        self.char_value = [False]*6
        self.table = dict(zip(
            "\n⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿",
            "\n A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="            
            ))
        self.reverse_table = {v: k for k, v in self.table.items()}
        self.switch('init')
        self.reset()
        Tools.write(self.IN, '|')

    @Tools.write_OUT
    def decode(self, IN):
        if self.reverse.value.get() == 'yes':
            return '|'+'|'.join(self.reverse_table.get(i.upper(), '_') for i in IN)+'|'
        else:
            return ''.join(self.table.get(i, '_') for i in IN[1:-1].split('|'))

    def switch(self, _):
        for i in (self.tab, self.IN, self.OUT, self.char, self.submit_button,
                  self.reset_button, self.reverse.input):#self.type.input, 
            if self.reverse.value.get() == 'yes' or _ == 'init':
                i.bind('<Key>', self.key_handler)
            else:
                i.unbind('<Key>')
                self.reset()
        Tools.write(self.IN, self.OUT.get('1.0', 'end-1c'))
        if self.reverse.value.get() == 'yes' or _ == 'init':
            self.IN.bind('<Control-v>', self.key_handler)
        else:
            self.IN['state'] = 'normal'
            self.IN.unbind('<Control-v>')
        self.decode()

    def key_handler(self, key):
        if key.keycode == 22:
            self.IN['state'] = 'normal'
            try:
                self.IN.delete('sel.first', 'sel.last')
                text = self.IN.get('1.0', 'end-1c').replace('|', '')
                self.IN.delete('1.0', 'end')
                self.IN.insert('1.0', '|'+'|'.join(text)+'|')
            except Exception:
                self.IN.delete('end-3c', 'end')
            if self.IN.get('1.0', 'end-1c') == '':
                self.IN.insert('end', '|')
            self.IN['state'] = 'disabled'
        elif key.keycode in (36, 104):
            self.submit()
        elif key.keycode == 90:
            self.reset()
        elif key.keycode in (80,81,84,85,88,89):
            d = {88: 2, 89: 5, 84: 1, 85: 4, 80: 0, 81: 3}
            self.char_value[d[key.keycode]] = not self.char_value[d[key.keycode]]
            Tools.write(self.char, chr(10240+sum(j*2**i for i,j in enumerate(self.char_value))))
        elif key.keycode == 55 and key.state == 20:
            text = ''.join(i for i in self.IN.selection_get(selection='CLIPBOARD') if i in self.table)
            try:
                self.IN['state'] = 'normal'
                self.IN.insert('sel.first', text)
                self.IN.delete('sel.first', 'sel.last')
                text = self.IN.get('1.0', 'end-1c').replace('|', '')                       
            except Exception:
                text = self.IN.get('1.0', 'end-1c').replace('|', '')+''.join(text)
            Tools.write(self.IN, '|'+'|'.join(text)+'|')

    def submit(self):
        Tools.write(self.IN, self.IN.get('1.0', 'end-1c')+self.char.get('1.0', 'end-1c')+'|')
        self.reset()
        self.decode()

    def reset(self):
        self.char_value = [False]*6
        Tools.write(self.char, '⠀')

class Caesar():
    def __init__(self):
        Tools.make_tab(self, 'Caesar')
        self.Rot = Tools.make_input(self, 5, 'Rotation (0=all):', '13', ttk.Entry, validate='key', width=5,
                                    validatecommand = (root.register(self.validate), '%P'))
        Tools.make_reverse(self, 7)

    @Tools.write_OUT
    def decode(self, IN):
        if self.Rot.value.get() == '':
            return ''
        Rot = int(self.Rot.value.get())
        if self.reverse.value.get() == 'yes':
            Rot = (26 - Rot) % 26
        if Rot == 0:
            return '\n\n'.join(f'__Rot:{str(i).ljust(74,"_")}\n{self.Caesar(IN,i)}' for i in range(1,26))
        else:
            return self.Caesar(IN, Rot)

    def Caesar(self, IN, Rot):
        OUT = ''
        for j in IN:
            if ord(j) in range(65,91):
                OUT += chr((ord(j)-65+Rot)%26+65)
            elif ord(j) in range(97,123):
                OUT += chr((ord(j)-97+Rot)%26+97)
            else:
                OUT += j
        return OUT

    def validate(self, value):
        if value == '':
            return True
        try:
            value = int(value)
        except ValueError:
            return False
        if value > 25 or value < 0:
            return False
        if value == 0:
            self.reverse.value.set('no')
            self.reverse.input['state'] = 'disabled'
            self.reverse.input.unbind('<ButtonRelease>')
        elif str(self.reverse.input['state']) == 'disabled':
            self.reverse.input['state'] = 'normal'
            self.reverse.input.bind('<ButtonRelease>', lambda _ : Tools.switch(self))
        return True

class Filter():
    def __init__(self):
        Tools.make_tab(self, ' Filter ')

        self.type_value = tk.StringVar()
        self.type_value.set('index (spaces)')
        self.type_value.trace_add('write', self.decode)
        self.type_input = ttk.Combobox(self.tab, textvariable=self.type_value, width=16, state='readonly',
                                       values=('index (spaces)', 'index (no spaces)', 'character'))
        self.type_input.grid(column=6, row=2, sticky='E')

        self.filter_value = tk.StringVar()
        self.filter_value.trace_add('write', self.decode)
        self.filter_input = ttk.Entry(self.tab, textvariable=self.filter_value, validate='key',
                                      width=5, validatecommand = (root.register(self.validate), '%P'))
        self.filter_input.grid(column=7, row=2, sticky='W')


    @Tools.write_OUT
    def decode(self, IN):
        if self.filter_value.get() == '':
            return ''
        if self.type_value.get() == 'index (spaces)':
            return ''.join(o if (i+1)%int(self.filter_value.get())!=0 else '' for i,o in enumerate(IN))
        elif self.type_value.get() == 'index (no spaces)':
            OUT = ''
            i = 1
            for o in IN:
                if o in ' \n\r\t':
                    OUT += o
                else:
                    if i%int(self.filter_value.get())!=0:
                        OUT += o
                    i += 1
            return OUT
        return IN.replace(self.filter_value.get(), '')

    def validate(self, value):
        if value == '':
            return True
        if 'index' in self.type_value.get():
            return value.isdecimal()
        return len(value) == 1

class Morse():
    def __init__(self):
        Tools.make_tab(self, 'Morse')
        self.dit = Tools.make_input(self, 2, 'dit (.)', '.', ttk.Entry, width=5)
        self.dah = Tools.make_input(self, 4, 'dah (-)', '-', ttk.Entry, width=5)
        self.letter = Tools.make_input(self, 6, 'letter sep', ' ', ttk.Entry, width=5)
        self.word = Tools.make_input(self, 8, 'word sep', '\\', ttk.Entry, width=5)
        Tools.make_reverse(self, 10)

    @Tools.write_OUT
    def decode(self, IN):
        alphabet = {'.-'   : 'a', '-...' : 'b', '-.-.' : 'c', '-..'  : 'd', '.'    : 'e',
                    '..-.' : 'f', '--.'  : 'g', '....' : 'h', '..'   : 'i', '.---' : 'j',
                    '-.-'  : 'k', '.-..' : 'l', '--'   : 'm', '-.'   : 'n', '---'  : 'o',
                    '.--.' : 'p', '--.-' : 'q', '.-.'  : 'r', '...'  : 's', '-'    : 't',
                    '..-'  : 'u', '...-' : 'v', '.--'  : 'w', '-..-' : 'x', '-.--' : 'y',
                    '--..' : 'z', ''     : '' , '\\'   : ' ', '\n'   : '\n',
                    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
                    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'}

        char = {self.dit.value.get():'.', self.dah.value.get():'-', ' \n ':'\n', '\n':' \n ', 
                self.letter.value.get():' ', self.word.value.get():'\\'}

        if self.reverse.value.get() == 'yes':
            alphabet = {v: k for k, v in alphabet.items()}
            char = {v: k for k, v in char.items()}
            IN = ' '.join(alphabet.get(i.lower(), '_') for i in IN).replace(' \n ', '\n')
            return ''.join(char.get(i, '_') for i in IN).replace(' \n ', '\n')
        else:
            IN = ''.join(char.get(i, '_') for i in IN)
            return ''.join(alphabet.get(i, '_') for i in IN.split(' '))

class Regex():
    def __init__(self):
        Tools.make_words_tab(self, 'Regex')
        self.type = Tools.make_input(self, 9, 'type:', 'match', ttk.Combobox, trace=False, width=7,
                                      state='readonly', values=('match', 'bigger'))

    @Tools.write_words_OUT
    def decode(self, IN, Words):
        if self.type.value.get() == 'match':
            return [i for i in Words if bool(re_search(f'^{IN}$',i))]
        else:
            return [i for i in Words if bool(re_search(IN,i))]

class Vigenere():
    def __init__(self):
        Tools.make_tab(self, 'Vigenere')
        self.key = Tools.make_input(self, 5, 'key:', '', ttk.Entry, width=20)
        Tools.make_reverse(self, 7)

    @Tools.write_OUT
    def decode(self, IN):
        if self.key.value.get() == '':
            return ''
        Key = [ord(i)-64 for i in self.key.value.get().upper()]
        if self.reverse.value.get() == 'yes':
            Key = [-i for i in Key]
        return ''.join(chr((ord(j.upper())-65+Key[i%len(Key)])%26+65+(32*j.islower()))
                       if ord(j.upper()) in range(65,91) else j for i,j in enumerate(IN))

class Python:
    def __init__(self):
        self.tab = ttk.Frame(tabControl)
        self.tab.pack()
        tabControl.add(self.tab, text='Python')
        #from idlelib import pyshell
        #pyshell.use_subprocess = True
        #sh = pyshell.PyShell()
        #sh.text.grid(in_=self.tab, column=1, row=1)
        #sh.begin()

class Info:
    def __init__(self):
        self.tab = ttk.Frame(tabControl)
        self.tab.pack()
        tabControl.add(self.tab, text='  Info  ')

        self.pad = tk.Label(self.tab, font=('Times 7'))
        self.pad.grid(column=1, row=1, columnspan=12)

        self.lang = Tools.make_input(self, 6, 'Language/Sprache:', 'English', ttk.Combobox, width=7,
                                     trace=False, state='readonly', values=('English', 'Deutsch'))
        self.lang.value.trace_add('write', self.change_lang)
        
        def scroll(self, *args, event=None):
            if event is None:
                self.text.yview(*args)
            else:
                self.text.yview_scroll(-event.delta//36, 'unit')
            return 'break'

        self.scrollbar = ttk.Scrollbar(self.tab, orient='vertical', command=lambda *args:scroll(self, *args))
        self.scrollbar.grid(column=12, row=3, sticky='NS')
        
        self.text = tk.Text(self.tab, height=41, width=78, state='disabled', bg='grey95', bd=0,
                            yscrollcommand=self.scrollbar.set)
        self.text.grid(column=1, row=3, columnspan=11, sticky='S', padx=(27,0), pady=15)
        self.text.bind('<MouseWheel>', lambda event:scroll(self, event=event))

        self.change_lang()

    def change_lang(self, *_):
        if self.lang.value.get() == 'English':
            with open('infoEng.txt', 'r', encoding='utf-8') as f:
                Text = f.read()
        else:
            with open('infoGer.txt', 'r', encoding='utf-8') as f:
                Text = f.read()
        Tools.write(self.text, Text)
        self.parse(self.text, Text)

    def parse(self, obj, Text):
        obj.tag_configure('h1', font=('TkFixedFont',15,'bold'))
        obj.tag_configure('h2', font=('TkFixedFont',10,'bold'))
        for i,o in enumerate(Text.split('\n')):
            if o == '':
                continue
            if o[0] != ' ':#headlines
                obj.tag_add('h1', f'{i+1}.0', f'{i+1}.end')
            elif ':' in o:
                if o[2] != ' ':#keywords with indent 2
                    obj.tag_add('h2', f'{i+1}.2', f'{i+1}.{o.index(":")}')
                else:#keywords with indent 4
                    obj.tag_add('h2', f'{i+1}.4', f'{i+1}.{o.index(":")}')

tabControl = ttk.Notebook(root)
Tabs = [Annagram(),    Ascii(),   Atbash(),     Base(),  Braille(),   Caesar(),
          Filter(),    Morse(),    Regex(), Vigenere(),   Python(),     Info()]
tabControl.pack(fill='both', expand=1)

print('''Tabs: OUT/_OUT
 0 Annagram
 1 Ascii
 2 Atbash
 3 Base
 4 Braille
 5 Caesar
 6 Filter
 7 Morse
 8 Regex
 9 Vigenere
10 Python
11 Info''')

root.mainloop()

# TODO
# python
# braille curser
#   move cursor (mouse / arrow keys)
#   -> and entf key
# Info.parse
