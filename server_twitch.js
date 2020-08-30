const tmi = require("tmi.js");
const keyHandler = require("./keyHandler.js");
const config = require("./config.js");

// https://github.com/tmijs/tmi.js#tmijs
// for more options
const client = new tmi.client({
  connection: {
    secure: true,
    reconnect: true,
  },
  channels: [config.channel],
});


var commandRegex = config.regexCommands

client.on("message", function (channel, tags, message, self) {
  let isCorrectChannel = `#${config.channel}` === channel;
  console.log('Received message: ', message)
  let messageMatches = message.match(commandRegex);

  if (self) return;
  if (isCorrectChannel && messageMatches) {
    // print username and message to console
    console.log(`@${tags.username}: ${message}`);
    // separate into command and hold time
    key = messageMatches[1]
    hold_time = messageMatches[3]
    // send the message to the emulator
    keyHandler.sendKey(key.toLowerCase(), hold_time);
  }
});

client.addListener("connected", function (address, port) {
  console.log("Connected! Waiting for messages..");
});
client.addListener("disconnected", function (reason) {
  console.log("Disconnected from the server! Reason: " + reason);
});

client.connect();
if (config.channel === 'twitchplayspokemon') {
  console.log("");
  console.log("'twitchplayspokemon' is the default channel! Otherwise, run with the environment variable: ");
  console.log("TWITCH_CHANNEL=mychannelhere npm start");
  console.log("");
}
console.log(`Connecting to /${config.channel}..`);