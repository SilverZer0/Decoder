function makeLabel(tab, labelText){
    let label = document.createElement("label");
    label.innerHTML = labelText;
    tab.tab.getElementsByTagName("tab-settings")[0].appendChild(label);
    return label;
}

function makeSelect(tab, labelText, ...values){
    let select = document.createElement("select");
    for(let value of values){
        let option = document.createElement("option");
        option.innerHTML = value;
        select.add(option);
    }
    select.oninput = ()=>{tab.decode();tab.IN.focus()};
    if(labelText){makeLabel(tab, labelText).appendChild(select)};
    return select;
}

function makeTextInput(tab, labelText, defaultValue, validation){
    let textInput = document.createElement("input");
    textInput.type = "text";
    textInput.value = defaultValue;
    textInput.savedValue = defaultValue;
    textInput.classList.add("short-text")
    textInput.addEventListener("input", ()=>{
        if(textInput.value == "" || RegExp(validation).test(textInput.value)){
            textInput.savedValue = textInput.value;
            if(textInput.value){tab.decode();}
        }else{
            textInput.value = textInput.savedValue;
        }
    })

    if(labelText){makeLabel(tab, labelText).appendChild(textInput)};
    return textInput;
}

function makeCheckbox(tab, labelText){
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.onclick = ()=>{tab.decode();tab.IN.focus();};
    if(labelText){makeLabel(tab, labelText).appendChild(checkbox)};
    return checkbox
}

function makeReverse(tab){
    tab.reverse = makeCheckbox(tab, "reverse: ");
    tab.reverse.onclick  = ()=>{
        tab.IN.value = tab.OUT.value;
        tab.decode();
        tab.IN.focus();
    };
}

function makeButton(tab, text, onclickFunction){
    let button = document.createElement("button");
    button.innerHTML = text;
    button.onclick = onclickFunction;
    tab.tab.getElementsByTagName("tab-settings")[0].appendChild(button);
    return button
}

class Tab{
    constructor(name, colOUT = false){
        this.tabbutton = document.createElement("button");
        this.tabbutton.id = name + "-button";
        this.tabbutton.innerHTML = name;
        this.tabbutton.onclick = ()=>{
            if(this.tabbutton.classList.contains("active")){
                jumpToInfo(this.tabbutton.id.replace("-button", "-info"))
                return;
            }
            loadTab(this)
        };
        tabbar.appendChild(this.tabbutton);

        let tooltip = document.createElement("span");
        tooltip.className = "tooltip";
        tooltip.innerHTML = "Click again to jump to Help";
        this.tabbutton.appendChild(tooltip)

        this.tab = document.createElement("tab-content");
        this.tab.id = name;

        var settings = document.createElement("tab-settings")
        this.tab.appendChild(settings);
        if(colOUT){
            var container = document.createElement("div");
            settings.appendChild(container);

            this.IN = document.createElement("input");
            this.IN.type = "text";
            this.IN.classList.add("IN");
            this.IN.addEventListener("keydown", 
                (key)=>{if(key.code == "Enter"){this.decode()}}
            );
            container.appendChild(this.IN);

            var search = document.createElement("button");
            search.innerHTML = "Search";
            search.onclick = (e)=>{this.decode(e.altKey)};
            container.appendChild(search);

            this.count = document.createElement("div");
            this.count.innerHTML = "0 Results";
            this.count.style = "width: 100px;text-align: right;"
            settings.appendChild(this.count);

            this.copy = makeButton(this, "copy", ()=>{
                try{
                    navigator.clipboard.writeText(this.OUT.value.join("\n"))
                }catch{
                    let data = document.createElement('input')
                    data.style = "display:none"
                    this.copy.append(data)
                    data.value = this.OUT.value.join("\n")
                    data.select()
                    document.execCommand("copy");
                    data.remove()
                }})

            this.OUT = {};
            this.OUT.div = document.createElement("div");
            this.OUT.div.classList.add("columns");
            this.OUT.value = [];
            var outerDiv = document.createElement("div");
            outerDiv.classList.add("container");
            outerDiv.appendChild(this.OUT.div);
            this.tab.appendChild(outerDiv);
        }else{
            this.IN = document.createElement("textarea");
            this.IN.addEventListener("input", ()=>{this.decode()});
            this.IN.rows = 20;
            this.IN.cols = 105;
            this.IN.classList.add("margin-top");
            this.tab.insertBefore(this.IN, settings);

            this.OUT = document.createElement("textarea");
            this.OUT.rows = 30;
            this.OUT.cols = 105;
            this.OUT.readOnly = true;
            this.tab.appendChild(this.OUT);
        }
        content.appendChild(this.tab);
    }
}

class Anagram extends Tab{
    constructor(){
        super("Anagram", true);
        this.source = makeSelect(this, "Source: ", "WordsEng", "OUT_Anagram", "OUT_Regex");
        this.type = makeSelect(this, "type: ", "match", "bigger", "smaller");
        //remove Listeners
        this.source.oninput = ()=>{};
        this.type.oninput = ()=>{};
    }

    decode(force){
        var Words = getWords(this.source.value);
        var input = this.IN.value.toLowerCase().split("").sort();
        switch(this.type.value){
            case "match":
                this.OUT.value = Words.filter((v)=>{return v.length == input.length 
                    && v.toLowerCase().split("").sort().every((v,i)=>{return v == input[i]})});
                break;
            case "bigger":
                this.OUT.value = Words.filter((v)=>{return v.length >= input.length 
                    && this.isSublist(v.toLowerCase().split("").sort(), input)});
                break;
            case "smaller":
                this.OUT.value = Words.filter((v)=>{return v.length <= input.length 
                    && this.isSublist(input, v.toLowerCase().split("").sort())});
        }
        
        this.count.innerHTML = this.OUT.value.length + " Results";
        this.OUT.div.innerHTML = "";

        if(this.OUT.value.length > 10_000 && !force){return}
        
        for(let word of this.OUT.value){
            var span = document.createElement("span");
            span.innerHTML = word;
            this.OUT.div.appendChild(span);
        }
    }

    isSublist(container, content){
        //does content fit into container?
        var i, j;
        for (i=0,j=0; i<container.length && j<content.length;) {
            if (container[i] < content[j]) {
                ++i;
            } else if (container[i] == content[j]) {
                ++i; ++j;
            } else {
                return false;
            }
        }
        return j == content.length;
    }
}

class Ascii extends Tab{
    constructor(){
        super("Ascii");
        this.type = makeSelect(this, "type: ", "1-26 dec", "1-26 bin", "1-26 hex","ascii dec", "ascii bin", "ascii hex")
        makeReverse(this);
    }

    decode(){
        var nonAscii = this.type.value.includes("1-26");
        var base = {"bin":2, "dec":10, "hex":16}[this.type.value.split(" ")[1]];
        if(this.reverse.checked){
            this.OUT.value = this.IN.value.toUpperCase().split("").map((v) => {
                return "\n\r\t ".includes(v) ? v : 
                (v.charCodeAt(0) - 64 * nonAscii).toString(base).padStart(8 * (base == 2), "0");
            }).join(" ").replaceAll(" \n ", "\n");
        }else{
            this.OUT.value = this.IN.value.toLowerCase().replaceAll("\n", " \n ").split(" ").map((v) => {
                if("\n\r\t ".includes(v)){return v}
                var base10 = parseInt(v, base);
                if(base10.toString(base) == v.replace(/^0+/, "")){
                    return String.fromCharCode(base10 + 64 * nonAscii)
                }
                return "_";
            }).join("");
        }
    }
}

class Atbash extends Tab{
    constructor(){
        super("Atbash");
        makeButton(this, "switch", ()=>{
            tab.IN.value = tab.OUT.value;
            tab.decode();
            tab.IN.focus();
        })
        this.alphabet = new Map([
            ['A', 'Z'], ['B', 'Y'], ['C', 'X'], ['D', 'W'], ['E', 'V'],
            ['F', 'U'], ['G', 'T'], ['H', 'S'], ['I', 'R'], ['J', 'Q'],
            ['K', 'P'], ['L', 'O'], ['M', 'N'], ['N', 'M'], ['O', 'L'],
            ['P', 'K'], ['Q', 'J'], ['R', 'I'], ['S', 'H'], ['T', 'G'],
            ['U', 'F'], ['V', 'E'], ['W', 'D'], ['X', 'C'], ['Y', 'B'],
            ['Z', 'A'],
            ['a', 'z'], ['b', 'y'], ['c', 'x'], ['d', 'w'], ['e', 'v'],
            ['f', 'u'], ['g', 't'], ['h', 's'], ['i', 'r'], ['j', 'q'],
            ['k', 'p'], ['l', 'o'], ['m', 'n'], ['n', 'm'], ['o', 'l'],
            ['p', 'k'], ['q', 'j'], ['r', 'i'], ['s', 'h'], ['t', 'g'],
            ['u', 'f'], ['v', 'e'], ['w', 'd'], ['x', 'c'], ['y', 'b'],
            ['z', 'a']]);
    }

    decode(){
        this.OUT.value = this.IN.value.split("").map((v) => {
            return this.alphabet.has(v) ? this.alphabet.get(v) : v;
        }).join("");
    }
}

class Base extends Tab{
    constructor(){
        super("Base");
        this.IN_Base = makeTextInput(this, "IN-Base: ", "2", "^([1-9]|[12][0-9]|3[0-6])$");
        makeButton(this, "switch", ()=>{
            this.IN_Base.value = this.OUT_Base.value;
            this.OUT_Base.value = this.IN_Base.savedValue;
            this.IN_Base.savedValue = this.IN_Base.value;
            this.OUT_Base.savedValue = this.OUT_Base.value;
            this.IN.value = this.OUT.value;
            this.decode();
            this.IN.focus();
        })
        this.OUT_Base = makeTextInput(this, "OUT-Base:", "10", "^([1-9]|[12][0-9]|3[0-6])$");
    }
    decode(){
        var inBase = this.IN_Base.value;
        var outBase = this.OUT_Base.value;
        if(inBase == "1" || inBase == "" || outBase == "1" || outBase == ""){return}
        var data = this.IN.value.replaceAll("\n", " \n ").split(" ");
        data = data.map((v)=>{
            if("\n\r\t ".includes(v)){return v}
            var base10 = parseInt(v, inBase);
            if(base10.toString(inBase) == v.replace(/^0+/, "")){
                return base10.toString(outBase)
            }
            return "_";
        });
        this.OUT.value = data.join(" ").replaceAll(" \n ", "\n").replaceAll("NaN", "_");
    }
}

class Braille extends Tab{
    constructor(){
        super("Braille");
        this.submitButton = makeButton(this, "Submit", ()=>{this.submit();this.IN.focus()});

        this.resetButton = makeButton(this, "Reset", ()=>{this.reset();this.IN.focus()});
        this.char = document.createElement("div");
        for(let i=0;i<6;i++){
            if(i%3==0){
                var div = document.createElement("div")
                div.style = "display:inline-block;"
                this.char.appendChild(div);
            }
            var dot = document.createElement("input");
            dot.type = "checkbox";
            dot.id = "dot-" + i;
            dot.classList.add("braille-dot");
            div.appendChild(dot);
            div.appendChild(document.createElement("br"));
        }
        this.tab.getElementsByTagName("tab-settings")[0].appendChild(this.char);
        //this.type = makeSelect(this, "input ", "895623", "784512");
        makeReverse(this);
        this.reverse.addEventListener("click", ()=>{
            this.submitButton.disabled = this.reverse.checked;
            this.resetButton.disabled = this.reverse.checked;
            this.IN.readOnly = !this.reverse.checked;
            for(let dot of document.getElementsByClassName("braille-dot")){
                dot.disabled = this.reverse.checked
            }
            this.reset();
        })
        //this.IN.readOnly = true;
        this.IN.value = "|";

        this.IN.addEventListener("keydown", (key)=>{
            if(!this.tab.classList.contains("active") || this.reverse.checked
             ||! ( key.code == "Backspace" || key.code == "Enter"
                || key.code.includes("Numpad") )){return}
            key.stopPropagation();
            key.preventDefault();
            switch(key.code){
                case "Numpad8":
                case "Numpad5":
                case "Numpad2":
                case "Numpad9":
                case "Numpad6":
                case "Numpad3":
                    var dot = document.getElementById("dot-" + "852963".indexOf(key.code.slice(-1)));
                    dot.checked = !dot.checked;
                    break;
                case "Numpad0":
                    this.reset();
                    break;
                case "NumpadEnter":
                    this.submit();
                    break;
                case "Backspace":
                    this.IN.value = this.IN.value.slice(0,-2);
                    this.OUT.value = this.IN.value.slice(0,-1);
                    break;
                case "Enter":
                    this.IN.value += "\n|";
                    this.OUT.value += "\n";
            }
        })
        this.IN.addEventListener("paste", (event)=>{
            if(this.reverse.checked){return}
            var cleanText = event.clipboardData.getData("text").split("").filter(
                (v)=>{return this.alphabet.has(v) || (v && "\n\t\r".includes(v))}
            ).join("").trim();
            if(cleanText){
                this.IN.value += cleanText.split("").join("|") + "|";
            }
            event.preventDefault()
        })

        this.alphabet = new Map([
            ["⠀", " "], ["⠁", "A"], ["⠂", "1"], ["⠃", "B"], ["⠄", "'"], ["⠅", "K"],
            ["⠆", "2"], ["⠇", "L"], ["⠈", "@"], ["⠉", "C"], ["⠊", "I"], ["⠋", "F"],
            ["⠌", "/"], ["⠍", "M"], ["⠎", "S"], ["⠏", "P"], ["⠐", "\""], ["⠑", "E"],
            ["⠒", "3"], ["⠓", "H"], ["⠔", "9"], ["⠕", "O"], ["⠖", "6"], ["⠗", "R"],
            ["⠘", "^"], ["⠙", "D"], ["⠚", "J"], ["⠛", "G"], ["⠜", ">"], ["⠝", "N"],
            ["⠞", "T"], ["⠟", "Q"], ["⠠", ","], ["⠡", "*"], ["⠢", "5"], ["⠣", "<"],
            ["⠤", "-"], ["⠥", "U"], ["⠦", "8"], ["⠧", "V"], ["⠨", "."], ["⠩", "%"],
            ["⠪", "["], ["⠫", "$"], ["⠬", "+"], ["⠭", "X"], ["⠮", "!"], ["⠯", "&"],
            ["⠰", ";"], ["⠱", ":"], ["⠲", "4"], ["⠳", "\\"], ["⠴", "0"], ["⠵", "Z"],
            ["⠶", "7"], ["⠷", "["], ["⠸", "_"], ["⠹", "?"], ["⠺", "W"], ["⠻", "]"],
            ["⠼", "#"], ["⠽", "Y"], ["⠾", "]"], ["⠿", "="], ["\n", "\n"]]);
        this.reset()
    }

    decode(){
        if(this.reverse.checked){
            var alphabet = new Map();
            this.alphabet.forEach((v,k)=>{alphabet.set(v,k)});
            this.OUT.value = "|" + this.IN.value.split("").map((v)=>{
                v = alphabet.get(v.toUpperCase());
                return v != undefined ? v : "_";
            }).join("|") + "|"
        }else{
            var alphabet =this.alphabet;
            this.OUT.value = this.IN.value.slice(1,-1).split("|").map((v)=>{
                v = alphabet.get(v);
                return v != undefined ? v : "_";
            }).join("");
        }
    }

    submit(){
        this.IN.value += String.fromCodePoint(
            parseInt("10100000" + Array.from(
                document.getElementsByClassName("braille-dot"), (v)=>{return v.checked + 0}
            ).reverse().join(""), 2)
        ) + "|";
        this.reset();
        this.decode();
    }

    reset(){
        for(let dot of document.getElementsByClassName("braille-dot")){
            dot.checked = false;
        }
    }
}

class Caesar extends Tab{
    constructor(){
        super("Caesar");
        this.rot = makeTextInput(this, "Rotation (0=all): ", "13", "^-?[0-9]*$");
        makeReverse(this);
        this.rot.addEventListener('input', ()=>{
            if(this.rot.value == "0"){
                this.reverse.checked = false;
                this.reverse.disabled = true;
            }else{
                this.reverse.disabled = false;
            }
        })
        this.rot.addEventListener("blur", ()=>{
            this.rot.value = (this.rot.value % 26 + 26) % 26;
        })
    }

    decode(){
        var rot = this.rot.value
        if(this.reverse.checked){
            rot = (-rot + 26) % 26 
        }
        var text = this.IN.value;
        if(rot == 0){
            this.OUT.value = "";
            for(let i=1;i<26;i++){
                this.OUT.value += "_".repeat(47) + "Rot:" + i +"_".repeat(47+(i<10))
                 + "\n" + this.caesar(text, i) + "\n\n";
            }
        }else{
            this.OUT.value = this.caesar(text, parseInt(rot));
        }
    }   

    caesar(text, rot){
        return text.split("").map((v)=>{
            return /^[A-Za-z]$/.test(v) ? String.fromCharCode(
                (v.toUpperCase().charCodeAt(0) - 39 + rot) % 26 
                + 65 + 32 * (v == v.toLowerCase()) ) : v}).join(""); 
    }
}

class Filter extends Tab{
    constructor(){
        super("Filter");
        this.type = makeSelect(this, null, "delete index (space)", "delete index (no space)", 
            "leave index (space)", "leave index (no space)","character");
        this.filter = makeTextInput(this, null, "", {toString: ()=>{
            if(this.type.value == "character"){
                return ".+"
            }else{
                return "[0-9]+"}
            }});
        var div = document.createElement("div");
        div.appendChild(this.type);
        div.appendChild(this.filter);
        this.tab.getElementsByTagName("tab-settings")[0].appendChild(div);
    }

    decode(){
        var data = this.IN.value.split("");
        var filter = this.filter.value
        switch(this.type.value){
            case "delete index (space)":
            case "leave index (space)":
                data = data.filter((v, i)=>{
                    return Boolean((i+1) % filter) ^ (this.type.value == "leave index (space)")
                });
                break;
            case "leave index (no space)":
            case "delete index (no space)":
                var newData = [];
                let i = 0;
                for(let char of data){
                    if("\n\r\t ".indexOf(char) != -1){
                        newData.push(char)
                    }else{
                        if(Boolean((i+1) % filter) ^ (this.type.value == "leave index (no space)")){
                            newData.push(char)
                        }
                        i++;
                    }
                }
                data = newData;
                break;
            default /*"characters"*/:
                data = data.filter((v)=>{return v.toLowerCase()!=filter.toLowerCase()});
        }
        this.OUT.value = data.join("");
    }
    
}

class Morse extends Tab{
    constructor(){
        super("Morse");
        this.dit = makeTextInput(this, "dit (.) ", ".", "^.*$");
        this.dah = makeTextInput(this, "dah (-) ", "-", "^.*$");
        this.switchDitDah = makeButton(this, ". <=> -", ()=>{
            [this.dit.value, this.dah.value] = [this.dah.value, this.dit.value];this.decode()
        });
        this.letterSep = makeTextInput(this, "letter sep ", " ", "^.*$");
        this.wordSep = makeTextInput(this, "word sep ", "/", "^.*$");
        makeReverse(this);

        this.alphabet = new Map([
            [".-"   , "a"], ["-..." , "b"], ["-.-." , "c"], ["-.."  , "d"], ["."    , "e"],
            ["..-." , "f"], ["--."  , "g"], ["...." , "h"], [".."   , "i"], [".---" , "j"],
            ["-.-"  , "k"], [".-.." , "l"], ["--"   , "m"], ["-."   , "n"], ["---"  , "o"],
            [".--." , "p"], ["--.-" , "q"], [".-."  , "r"], ["..."  , "s"], ["-"    , "t"],
            ["..-"  , "u"], ["...-" , "v"], [".--"  , "w"], ["-..-" , "x"], ["-.--" , "y"],
            ["--.." , "z"], ["/"    , " "], ["\n"   , "\n"],
            ["-----", "0"], [".----", "1"], ["..---", "2"], ["...--", "3"], ["....-", "4"],
            [".....", "5"], ["-....", "6"], ["--...", "7"], ["---..", "8"], ["----.", "9"]]);

        this.char = {" \n ":"\n", "\n":" \n "};
    }

    decode(){
        var data = this.IN.value.split("");

        var char = Object.assign({}, this.char);
        if(this.reverse.checked){
            var alphabet = new Map();
            this.alphabet.forEach((v,k)=>{alphabet.set(v,k)});
            char["."] = this.dit.value;
            char["-"] = this.dah.value;
            char[" "] = this.letterSep.value;
            char["/"] = this.wordSep.value;

            this.OUT.value = data.map((v)=>{
                v = alphabet.get(v.toLowerCase());
                return v != undefined ? v : "_";
            }).join(" ").replaceAll(" \n ", "\n").split("").map((v)=>{
                v = char[v.toLowerCase()];
                return v != undefined ? v : "_";
            }).join("").replaceAll(" \n ", "\n");
        }else{
            var alphabet = this.alphabet;
            char[this.dit.value]       = ".";
            char[this.dah.value]       = "-";
            char[this.letterSep.value] = " ";
            char[this.wordSep.value]   = "/";

            this.OUT.value = data.map((v)=>{
                v = char[v];
                return v != undefined ? v : "_";
            }).join("").split(" ").map((v)=>{
                v = alphabet.get(v);
                return v != undefined ? v : "_";
            }).join("");
        }            
    }
}

class Regex extends Tab{
    constructor(){
        super("Regex", true);
        this.source = makeSelect(this, "Source: ", "WordsEng", "OUT_Anagram", "OUT_Regex");
        this.type = makeSelect(this, "type: ", "match", "bigger");
        //remove Listeners
        this.source.oninput = ()=>{};
        this.type.oninput = ()=>{};
    }

    decode(force){
        this.count.innerHTML = "Loading ...";
        var Words = getWords(this.source.value);
        var regex = this.IN.value;
        if(this.type.value == "match"){
            regex = "^" + regex + "$";
        }
        this.OUT.value = Words.filter((v)=>{return RegExp(regex, "i").test(v)});
        
        this.count.innerHTML = this.OUT.value.length + " Results";
        this.OUT.div.innerHTML = "";

        if(this.OUT.value.length > 10_000 && !force){return}
        
        for(let word of this.OUT.value){
            var span = document.createElement("span");
            span.innerHTML = word;
            this.OUT.div.appendChild(span);
        }
    }
}

class Tapcode extends Tab{
    constructor(){
        super("Tapcode");
        this.type = makeSelect(this, "abc: ", "c&k = c", "i&j = i");
        this.type.addEventListener("input", (e)=>{
            if(this.type.value == "c&k = c"){
                this.ABC = "ABCDEFGHIJLMNOPQRSTUVWXYZ"
            }else{
                this.ABC = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
            }
        })
        this.switchXY = makeCheckbox(this, "switch xy:");
        makeReverse(this);
        this.ABC = "ABCDEFGHIJLMNOPQRSTUVWXYZ"
    }

    decode(){
        if(this.reverse.checked){
            var data = this.IN.value.split("");
            data = data.map((value)=>{
                if("\n\r\t ".includes(v)){return value}
                var index = this.ABC.indexOf(value);
                if(index == -1){return "_"}
                var remainder = index % 5
                if(this.switchXY.checked){
                    return remainder*10 + (index-remainder)/5 + 11;
                }
                return (index-remainder)*2 + remainder + 11;
            })
            this.OUT.value = data.join("");
        }else{
            var data = this.IN.value.replaceAll("\n"," \n ").split(" ");
            data = data.map((value)=>{
                if("\n\r\t ".includes(value)){return value}
                if(value.length != 2){return "_"}
                return this.ABC[(value[this.switchXY.checked+0] * 1 - 1) * 5 
                    + value[!this.switchXY.checked+0] * 1 -1] || "_";
            })
            this.OUT.value = data.join(" ").replaceAll(" \n ", "\n");
        }
    }
}
          
class Vigenere extends Tab{
    constructor(){
        super("Vigenere");
        this.key = makeTextInput(this, "key: ", "", "^[a-zA-Z]*$"); 
        this.key.classList.remove("short-text");
        makeReverse(this);
    }

    decode(){
        if(!this.key.value){
            this.OUT.value = this.IN.value;
            return;
        }
        var key = this.key.value.split("").map((v)=>{
            return (v.toUpperCase().charCodeAt(0) - 65) * (this.reverse.checked ? -1 : 1)
        })
        this.OUT.value = this.IN.value.split("\n").map((v)=>v.split("").map((v,i)=>{
            return /^[A-Za-z]$/.test(v) ? String.fromCharCode(
                (v.toUpperCase().charCodeAt(0) - 39 + key[i % key.length]) % 26 
                + 65 + 32 * (v == v.toLowerCase()) ) : v}).join("")).join("\n");        
    }
}

class Info{
    constructor(){
        this.tabbutton = document.createElement("button");
        this.tabbutton.id = "Info-button";
        this.tabbutton.innerHTML = "Info";
        this.tabbutton.onclick = ()=>{
            if(this.tabbutton.classList.contains("active")){
                document.getElementById("info-top").scrollIntoView();
                return;
            }
            loadTab(this)
        };
        tabbar.appendChild(this.tabbutton);

        let tooltip = document.createElement("span");
        tooltip.className = "tooltip";
        tooltip.innerHTML = "Click again to jump to the Top";
        this.tabbutton.appendChild(tooltip)

        this.tab = document.getElementById("info");

        for(let i of this.tab.getElementsByClassName("de")){
            i.classList.toggle("hidden");
        }

        let language = makeSelect(this, "Language / Sprache: ", "English", "Deutsch");
        language.oninput = ()=>{
            for(let i of this.tab.getElementsByClassName("en")){
                i.classList.toggle("hidden");
            }
            for(let i of this.tab.getElementsByClassName("de")){
                i.classList.toggle("hidden");
            }
        }

        this.IN = this.tab // loadTab needs IN to focus on
    }
}

var WordsEng = null;
fetch("./wordsEng.txt").then(
    response => response.text()).then(data => {
    WordsEng =  data.split('\n');
});

function getWords(source){
    switch(source){
        case "WordsEng":
            return WordsEng;
        case "OUT_Anagram":
            return Tabs[0].OUT.value;
        case "OUT_Regex":
            return Tabs[8].OUT.value;
    }
}

const tabbar = document.getElementById("tabbar")
const content = document.getElementById("tab-content")
const Tabs = [
    new  Anagram(), new    Ascii(), new   Atbash(),
    new     Base(), new  Braille(), new   Caesar(),
    new   Filter(), new    Morse(), new    Regex(),
    new  Tapcode(), new Vigenere(), new     Info()
]

function tabs(){
    console.clear();
    for(let [i, o] of Tabs.entries()){
        console.log(`${i} ${o.constructor.name}`);
    }
}

function loadTab(tab){
    for (let content of document.getElementById("tab-content").children) {
        content.className = "hidden";
    }
    for (let button of document.getElementById("tabbar").children) {
        button.className = "";
    }
    tab.tab.className = "";
    tab.tabbutton.className = "active";
    tab.IN.focus();
}

function jumpToInfo(target){
    Tabs[11].tabbutton.click();
    document.getElementById(target).scrollIntoView();
}

Tabs[0].tabbutton.click();
tabs();

/* Regex speed tests
 Query |results|time|render|
.*     | 466550|  - |      |
s.*    |  50571|  - | 24000|
r.*    |  21286|3000|  4300|
w.*    |  11672| 625|   -  |
[qxy].*|   5567| 250|   -  |
*/