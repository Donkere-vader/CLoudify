import json

f = json.load(open('.cloudify_settings.json'))

def set_globals():
    global IP, PORT, AUTH_KEY, SYNC_FOLDER, HEADERSIZE
    IP = f['ip']
    PORT = f['port']
    AUTH_KEY = f['auth_key']
    SYNC_FOLDER = f['sync_folder']
    HEADERSIZE = 10

set_globals()
