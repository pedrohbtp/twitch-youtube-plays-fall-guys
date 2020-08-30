let generalConfig = require('./config.json')
// change these two variables
let channel = generalConfig['twitch_channel']
let programName = generalConfig['program_name']
  
// builds the keymap
let keymap = generalConfig['key_mapping']
// List of commands to check for
let commands = Object.keys(generalConfig['key_mapping'])
// matches strings like <command> <number_optional>
let regexCommands = new RegExp("^(" + commands.join("|") + ")" + "( +)?([1-5]?)$", "i")

let filteredCommands = [];
let throttledCommands = [];
module.exports = {
  // regex commands used to parse
  regexCommands,
  // the keymap
  keymap,
  // all commands to print out
  commands,
  // twitch channel to connect to
  channel,
  // Title of the window of the program (ex: 'Desmume' or 'VBA')
  programName,

  // If you need to filter the commands sent to the program
  // Ex: democracy/anarchy since they don't affect the program itself
  // Ex: ["democracy","anarchy"]
  filteredCommands,

  // If you want to prevent people from using from command too often
  // Ex: ["start"]
  throttledCommands,

  // Throttle time in seconds
  // Ex: you can limit 'start' so it's only used every 10 sec
  timeToWait: 10000,

  // Delay between each possible keypress in milliseconds (can't be too fast)
  // To change on Windows, change `key.py`
  delay: 100,
};