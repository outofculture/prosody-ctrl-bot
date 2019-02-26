import asyncio
import random
import re

import aioxmpp
import aioxmpp.dispatcher

jidparams = {
    'jid': 'serverbot@outofinter.net',
    # 'password': 'fake',
}

my_jid = aioxmpp.JID.fromstr(jidparams['jid'])

with open('/usr/share/dict/words') as wordsfile:
    wordlist = wordsfile.read().split('\n')


def make_password():
    passwd = random.choice(wordlist)
    while len(passwd) < 20:
        passwd = '{} {}'.format(passwd, random.choice(wordlist))
    return passwd


def execute_prosody(command: str, *interactive_responses: str) -> bool:
    command = 'prosodyctl {}'.format(command)
    if re.search('[^-_ .0-9a-zA-Z]', command) or len(command) > 1023:
        # unsafe
        return False
    else:
        return False


async def main():
    client = aioxmpp.PresenceManagedClient(
        my_jid,
        aioxmpp.make_security_layer(jidparams['password']),
    )

    def message_response(msg):
        if not msg.body:
            return
        resp = msg.make_reply()
        command = msg.body.any()
        if command.lower().startswith('password'):
            new_password = command[len('password '):]
            if not new_password:
                resp.body[None] = 'Missing required information. Usage: "password [NEW PASSWORD]'
            else:
                successful = execute_prosody(
                    'passwd {}'.format(msg.from_),
                    new_password,
                    new_password,
                )
                if successful:
                    resp.body[None] = 'Password changed to "{}"'.format(new_password)
                else:
                    resp.body[None] = 'I failed at the one thing you asked of me -_-'
        elif command.lower().startswith('new user'):
            username = command[len('new user '):]
            if not username:
                resp.body[None] = 'Missing required information. Usage: "new user [USERNAME]'
            else:
                password = make_password()
                successful = execute_prosody(
                    'adduser {}@outofinter.net'.format(username),
                    password,
                    password,
                )
                if successful:
                    resp.body[None] = 'User {}@outofinter.net created. Tell them that their password is "{}"'.format(
                        username, password)
                else:
                    resp.body[None] = 'I failed at the one thing you asked of me -_-'
        else:
            resp.body[None] = 'I have no idea how to respond to that o_O'

        client.enqueue(resp)

    dispatch = client.summon(aioxmpp.dispatcher.SimpleMessageDispatcher)
    dispatch.register_callback(
        aioxmpp.MessageType.CHAT,
        None,
        message_response,
    )

    async with client.connected():
        while True:
            await asyncio.sleep(1)


# to_jid = 'martin@outofinter.net'
# text = 'test message from aio bot'

# import sys
#
# import nbxmpp
# from gi.repository import GObject as gobject
#
# # jid = nbxmpp.JID('serverbot@outofinter.net')
# # idle_queue = nbxmpp.idlequeue.get_idlequeue()
# # client = nbxmpp.NonBlockingClient(jid.getDomain(), idle_queue)
# # on_connect = lambda conn, conn_type: print('Connected with ', conn_type)
# # on_connect_failure = lambda: print('Could not connect')
# # client.connect(on_connect, on_connect_failure, secure_tuple=('tls', '', '', None, None))
#
#
#
# class Connection:
#     def __init__(self):
#         self.jid = nbxmpp.protocol.JID(jidparams['jid'])
#         self.password = jidparams['password']
#         self.sm = nbxmpp.Smacks(self)  # Stream Management
#         self.client_cert = None
#
#     def on_auth(self, conn, auth):
#         if not auth:
#             print('could not authenticate!')
#             sys.exit()
#         print('authenticated using ' + auth)
#         # self.send_message(to_jid, text)
#
#     def on_connected(self, con, con_type):
#         print('connected with ' + con_type)
#         self.client.auth(self.jid.getNode(), self.password, resource=self.jid.getResource(),
#                          sasl=1, on_auth=self.on_auth)
#
#     def get_password(self, callback, mech):
#         callback(self.password)
#
#     def on_connection_failed(self):
#         print('could not connect!')
#
#     def _event_dispatcher(self, realm, event, data):
#         pass
#
#     def connect(self):
#         self.idle_queue = nbxmpp.idlequeue.get_idlequeue()
#         self.client = nbxmpp.NonBlockingClient(self.jid.getDomain(), self.idle_queue, caller=self)
#         self.connection = self.client.connect(self.on_connected, self.on_connection_failed,
#                                               secure_tuple=('tls', '', '', None, None))
#
#     def send_message(self, to_jid, text):
#         id_ = self.client.send(nbxmpp.protocol.Message(to_jid, text, typ='chat'))
#         print('sent message with id ' + id_)
#         gobject.timeout_add(1000, self.quit)
#
#     def quit(self):
#         self.disconnect()
#         ml.quit()
#
#     def disconnect(self):
#         self.client.start_disconnect()
#
# conn = Connection()
# conn.connect()
# ml = gobject.MainLoop()
# # ml.run()
