var colourmapApp = new Vue({
    el: '#colormap'
    , methods: {
        colors(){
            return Object.assign({}, colormap)
        }
    }
})
