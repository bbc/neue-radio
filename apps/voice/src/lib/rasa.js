class Rasa {

    constructor() {
        // TODO Externalise to config;
        this.nluService = 'http://localhost:5005/';
    }

    getIntent(query, project, model) {
        console.log('Rasa:getIntent', query);
        return new Promise((resolve, reject) => {
            axios.post(this.nluService + 'parse', {
                'q': query,
                'project': project,
                'model': model
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