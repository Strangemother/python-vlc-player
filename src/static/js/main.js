var app = new Vue({
    el: '#main'
    , data: {
        last: {
            uri: 'D:/movies/Rising Damp/104  Night Out.divx'
        }
    }

    , methods: {
        load(uri) {
            console.log('Load', uri)
            this.post('load', {uri})
        }

        , post(action, data) {
            let d = Object.assign({action}, data)
            let o = {
                type: 'POST'
                , dataType: 'json'
                , url:'/request'
                , data: d
            }

            $.ajax(o)
        }

        , hit(path) {
            $.get(path)
        }
    }
})


var bus = new Vue({

})


