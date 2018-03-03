var inputApp = new Vue({
    el: '#question_input'
    , data: {
        question: 'hello'
        , lastQuestion: ''
        , messages: []
    }
    , mounted(){
        bus.$on('message', this.wsMessage.bind(this))
    }
    , methods: {

        wsMessage(data) {
            console.log('input from socket', data)
            let tokens = data.data.tokens
            if(tokens == undefined) { tokens = []}
            if(data.data.action) {
                this.messages.unshift({
                    action: data.data.action
                    , tokens: [].slice.call(tokens, 0)
                })
            }
        }

        , inputString(event) {
            console.log('Enter Key', this.question)
            this.lastQuestion = this.question
        }
    }
})
