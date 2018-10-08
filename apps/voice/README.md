### Neue Radio Voice

## Setup Rasa

`cd apps/voice`

`docker build -t rasa_server .`

`docker run --name rasa_server_ins -d -p 5005:5000 rasa_server`

## Train

`curl -XPOST -H "Content-Type: application/x-yml" localhost:5005/train?project=voice_hack --data-binary @assets/model.yml`

## Query

`curl -XPOST localhost:5005/parse -d '{"q":"play the radio", "project":"voice_hack"}'`

## Postman

`https://documenter.getpostman.com/view/924347/RWgozeGu`