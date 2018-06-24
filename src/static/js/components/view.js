Vue.component('tokenize', {
    template: $('.templates [data-for="tokenize"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
    , methods: {

        actionName(message) {
            let name = `action-${message.data.action}`
            if(Vue.options.components[name] != undefined) {
                return name;
            }
            return 'action-default'
        }
    }
});

Vue.component('assess', {
    template: $('.templates [data-for="assess"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }

    , methods: {

        actionName(message) {
            let name = `action-${message.data.action}`
            if(Vue.options.components[name] != undefined) {
                return name;
            }
            return 'action-default'
        }
    }
})

Vue.component('action-complete', {
    template: $('.templates [data-for="action-complete"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('default', {
    template: $('.templates [data-for="default"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('tokens-list', {
    template: $('.templates [data-for="tokens-list"]').remove()[0]
    , props: ['tokens']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-default', {
    template: $('.templates [data-for="action-default"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-start', {
    template: $('.templates [data-for="action-start"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})

Vue.component('action-word', {
    template: $('.templates [data-for="action-word"]').remove()[0]
    , props: ['message']
    , data: function(){
        return {

        }
    }
})
