const appName = window.location.pathname.replace(/\//g, '');
const websocket = createWebsocket();
const rasa = new Rasa();

const main = async () => {
  websocket.ready.then(() => {
    console.log('Websocket connected');

    websocket.publish({
      topic: `${appName}/event/ready`,
      payload: { msg: 'Internal app ready!' }
    });
  });

  websocket.subscribe(new RegExp(`${appName}/.*`), ({ topic, payload }) => {
    console.log('Recieved message', topic, payload);
    if (topic.includes("recognition")) {
      const type = payload.params.type;
      const transcript = payload.params.transcript;
      if (type === 'full') {
        rasa.getIntent(transcript).then((intent) => {
          console.log('Need to call publish', intent);
          if (intent === 'start_radio') {
            websocket.publish({ topic: `radio/command/hls` });
          } else if (intent === 'stop_radio') {
            websocket.publish({ topic: `radio/command/stop` });
          }
        }).catch(() => {
          console.log('intent not found');
        });
      }
    }
  });

  console.log('Internal app loaded');
};

main();
