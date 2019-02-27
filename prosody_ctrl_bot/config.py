import json
import os
from os.path import expanduser

import aioxmpp


conffilename = expanduser('~/.prosody-ctrl-bot.json')
if not os.path.exists(conffilename):
    conffilename = expanduser('/etc/prosody-ctrl-bot.json')

with open(conffilename) as conffile:
    jidparams = json.loads(conffile.read())

my_jid = aioxmpp.JID.fromstr(jidparams['jid'])
