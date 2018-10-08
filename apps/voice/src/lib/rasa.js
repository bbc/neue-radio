class Rasa {

    constructor() {
        // TODO Externalise to config;
        this.nluService = 'http://localhost:5005/';
    }

    getIntent(query, project) {
        console.log('Rasa:getIntent query', query);
        console.log('Rasa:getIntent project', project);
        return new Promise((resolve, reject) => {
            axios.post(this.nluService + 'parse', {
                'q': query,
                'project': project
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