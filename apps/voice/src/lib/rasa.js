class Rasa {

    constructor() {
        // TODO Externalise to config;
        this.nluService = 'http://localhost:5005/';
    }

    // TODO Add model lookup.
    getIntent(query) {
        console.log('Rasa:getIntent', query);
        return new Promise((resolve, reject) => {
            axios.post(this.nluService + 'parse', {
                'q': query,
                'project': 'current',
                'model': 'nlu'
            })
                .then(function (response) {
                    console.log('rasa request loaded', response.data.intent.name);
                    resolve(response.data.intent.name);
                })
                .catch(function (error) {
                    console.log('rasa request error', error);
                    reject('no intent found')
                });
        })
    }

}