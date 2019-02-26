import json
from os.path import expanduser

import aioxmpp


with open(expanduser('~/.prosody-ctrl-bot.json')) as conffile:
    jidparams = json.loads(conffile.read())

my_jid = aioxmpp.JID.fromstr(jidparams['jid'])
