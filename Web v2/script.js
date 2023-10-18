/*TODO
switch to Wordlist ordered by popularity
add option to switch between sorting type
move curent to filter tab
add analysis tab
 - display info like
   - letters for pos 1 sorted by apperence count
   - letters for full word sorted by apperence count
   ...
*/

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
    constructor(name, colOUT=false){
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

            this.copy = makeButton(this, "copy", ()=>{navigator.clipboard.writeText(this.OUT.value.join("\n"))})

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

class Words extends Tab{
    constructor(){
        super("Words", true)
        this.source = makeSelect(this, "Source: ", "WordsEng", "Results")
        this.regexType = makeSelect(this, "regex-type: ", "match", "bigger");
        this.AnagramType = makeSelect(this, "anagram-type: ", "match", "bigger", "smaller");
        //remove Listeners
        this.source.oninput = ()=>{};
        this.regexType = ()=>{};
        this.AnagramType = ()=>{};
    }

    decode(force){
        var Words = null;
        switch(this.source.value){
            case "WordsEng": 
                Words = WordsEng;
            case "Results": 
                Words = Tabs[0].OUT.value;
        }
    
        if(anagramIN){
            var input = this.IN.value.toLowerCase().split("").sort();
            switch(this.type.value){
                case "match":
                    Words = Words.filter((v)=>{return v.length == input.length 
                        && v.toLowerCase().split("").sort().every((v,i)=>{return v == input[i]})});
                    break;
                case "bigger":
                    Words = Words.filter((v)=>{return v.length >= input.length 
                        && this.isSublist(v.toLowerCase().split("").sort(), input)});
                    break;
                case "smaller":
                    Words = Words.filter((v)=>{return v.length <= input.length 
                        && this.isSublist(input, v.toLowerCase().split("").sort())});
            }
        }
        if(regexIN){
            var regex = this.IN.value;
            if(this.type.value == "match"){
                regex = "^" + regex + "$";
            }
            Words = Words.filter((v)=>{return RegExp(regex, "i").test(v)});
        }
        if(similarIN){
            //TODO add similar decode
        }
        
        this.OUT.value = Words;
        
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

var WordsEng = null;
fetch("./wordsEng.txt").then(
    response => response.text()).then(data => {
    WordsEng =  data.split('\n');
});