# Twitch/Youtube Plays Fall Guys

# installing the dependencies

```bash
npm install
pip install -r requirements.txt
```

# Configuration

Change ***config.json*** to point to the the Youtube/Twitch channel

# Running the servers

## Twitch

```bash
npm server_twitch.js
```

## Youtube

```bash
python server_yt.py
```

## Fall guys specific commands

Gets the input from the chat and converts into commands used in Fall Guys

Twitch/Youtube chat format: 
```
<action> <optional_hold_time_in_secons>
```
ex: up 5

will make walk forward for 5 seconds
if the hold time is not specified, it will just press it once
the hold time can currently be from 1 to 5

Commands:

* up: press button to go up
* down: press button to go down
* left: press button to go left
* right: press button to go right
* grab: press button to grab
* jump: press button to jump
* dive: press the button to dive
* esc: press the esc button



## The twitch logic is based on the following repository

https://github.com/hzoo/TwitchPlaysX