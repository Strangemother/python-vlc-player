
var main = function(){
    let wordView = new WordView()
    wordView.start('mynetwork')
    window.ww = wordView
}

var colormap = {
    'relatedto': '#dcdcdc'
    , 'isa': 'lightblue'
    // similat
    , 'synonym': '#57f09d'
    // opposite
    , 'antonym': 'purple'

    , '>>': 'red'
    , 'derived': 'pink'
}

class WordView {

    create(nodeId) {
        /* create the network view on the given element id*/
        var options = {};
        let data = this.getData()
        var container = document.getElementById(nodeId);
        var network = new vis.Network(container, data, options);
        return network;
    }

    start(name){
        this.network = this.create(name);
        bus.$on('message', this.wsMessage.bind(this))
    }

    wsMessage(data) {

        let sent = []
        let tokens = data.data.tokens || [];

        for(let l of tokens) {
            sent.push(l[0])
        }

        this.addWords(sent);

        if(data.data.ident) {
            //this.presentConceptNetResult(data)
        }

        if(data.data.word) {
            this.presentWord(data)
        }
    }

    presentWord(data) {
        let word = data.data.word;
        //this.addWord(word)
        //this.addWords()
        window.word = word
        let value = word.value;
        if(value == undefined) {
            console.warn(`Old data cache does not contain "value" attribte.
                Please delete dictionary file and update the cache.`)
            return
        }

        let iters = ['synonym', 'antonym']
        for (var j = 0; j < iters.length; j++) {
            if(word[iters[j]] == undefined) {
                console.log(`Word "${value}" does not have "${iters[j]}"`)
                continue
            }

            for (var i = 0; i < word[iters[j]].length; i++) {
                this.addRelate(value, word[iters[j]][i], iters[j])
            };
        }

        window.vpr = this
    }

    presentConceptNetResult(data){

        let metas = data.data.ident.meta;

        for(let meta of metas) {
            let end = meta.end.label.toLowerCase();
            let label = meta.rel.label.toLowerCase();
            let start = meta.start.label.toLowerCase();
            if( meta.end.language != 'en'
                || meta.start.language != 'en' ) {
                continue;
            }

            if(meta.weight < 1.4) {
                continue;
            }

            this.addRelate(start, end, label)
            this.addEdge(start, end, label)
        }

        console.log(data.data.type, Object.keys(data.data))
        console.log(data.data)
    }

    addWords(words, edgeLabel) {
        let last;

        for(let token of words) {
            let c = this.addWord(token.toLowerCase())
            if(last) {
                this.addEdge(last.toLowerCase(), token.toLowerCase(), edgeLabel)
            }
            last = token
        }

    }

    nodes(){
        if(this._nodes == undefined ) {
            this._nodes = new vis.DataSet([])
        };

        return this._nodes;
    }

    edges(){
        if(this._edges == undefined ) {
            this._edges = new vis.DataSet([])
        };

        return this._edges;
    }

    addWord(word){
        word = word.toLowerCase()
        if(word[0] == 'a') {
            let _word = word.split(' ').slice(1).join(' ')

            if(_word != '') {
                word = _word;
            }
        }

        if(word.split(' ').length > 1) {

            return this.addWords(word.split(' '), 'derived')
        }

        let nodes = this.nodes();
        let enode = nodes.get(word);
        if(enode != null) return enode;
        return nodes.add({
            id: word
            , label: word
            , color: '#EEE'
            , shape: 'box'
        })
    }

    addEdge(a, b, related='>>') {
        let edges = this.edges();
        related = related.toLowerCase()
        let eedge = edges.get(`${a}${b}`);
        if(eedge != null) return eedge;

        let cmap = colormap[related];
        let cl = cmap;
        if(typeof(cmap) == 'string') {
            cmap = {}
        } else {
            cl = cmap.color;
        }

        this.edges().add(Object.assign({
            id:`${a}${b}`
            , from:a
            , to: b
            , color: cl || '#DDD'
            // , value: .1
            , arrows: {
                to: {
                    scaleFactor: .4
                }
            }
            , label: colormap[related] == undefined? related: undefined
            , related: related
        }, cmap))
    }

    addRelate(word, relate, label='relatedTo') {
        /*
            Add a word related to another word, connecting an edge with an
            arrow pointing to relate (B)
         */
        /* append a 'relateTo', a related to b */
        this.addWord(word.toLowerCase())
        this.addWord(relate.toLowerCase())
        this.addEdge(word.toLowerCase(), relate.toLowerCase(), label)
    }

    getData(){

        // create a network
        var data = {
            nodes: this.nodes()
            , edges: this.edges()
        };

        return data;
    }
}

;main();
