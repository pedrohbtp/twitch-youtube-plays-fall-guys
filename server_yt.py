from pytchat import LiveChat
import re
import time
import key
import json

conf = {}
with open('config.json', 'r') as f:
    conf = json.load(f)

# import the window name from the configuration
window_name = conf['program_name']

key_mapping = conf['key_mapping']
# import the commands from the configuration
commands = list(key_mapping.keys())
#TODO: import the regex from the configuration
compiled_re = re.compile("^(" + '|'.join(commands) + ")( +)?([1-5]?)$")

def main():
    print('starting main')
    livechat = LiveChat(video_id = conf["youtube_video_id"])#, callback = treat_messages)
    while livechat.is_alive():
        try:
            treat_messages(livechat.get())
            # print('chat live')
        except KeyboardInterrupt:
            livechat.terminate()
            break
        except Exception as e:
            print('Exception: ', e)

def execute_command(message):
    
    matched_string = compiled_re.match(message)
    if matched_string != None:
        # command matched
        command = matched_string.groups()[0]
        print(matched_string.groups())
        if matched_string.groups()[2] != '':
                key.send_key_to_window(window_name=window_name, key=key_mapping[command], hold_time_seconds=float(matched_string.groups()[2]))
        elif matched_string.groups()[0] != None:
                key.send_key_to_window(window_name=window_name, key=key_mapping[command], hold_time_seconds=None)

#callback function (automatically called)
def treat_messages(chatdata):
    print('all items: ', chatdata.items)
    for c in chatdata.items:
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        execute_command(c.message)
        chatdata.tick()

if __name__ == '__main__':
    main()