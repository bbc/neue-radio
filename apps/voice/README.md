### Neue Radio Voice

## Setup Rasa

```cd apps/voice```

```docker build -t rasa_server .```

```docker run --name rasa_server_ins -d -p 5005:5000 rasa_server```

## Train

```curl -XPOST -H "Content-Type: application/x-yml" localhost:5005/train?project=voice_hack --data-binary @assets/model.yml```

```
{
    "intent": {
        "name": "start_radio",
        "confidence": 0.9729545712471008
    },
    "entities": [],
    "intent_ranking": [
        {
            "name": "start_radio",
            "confidence": 0.9729545712471008
        },
        {
            "name": "stop_radio",
            "confidence": 0.02402161806821823
        }
    ],
    "text": "play the radio",
    "project": "voice_hack",
    "model": "model_20181008-201438"
}
```

## Query

```curl -XPOST localhost:5005/parse -d '{"q":"play the radio", "project":"voice_hack"}'```

## Postman

```https://documenter.getpostman.com/view/924347/RWgozeGu```