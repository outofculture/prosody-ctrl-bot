import asyncio

import aioxmpp
import aioxmpp.dispatcher

jidparams = {
    'jid': 'serverbot@outofinter.net',
    # 'password': 'fake',
}

to_jid = 'martin@outofinter.net'
text = 'test message from aio bot'

jid = aioxmpp.JID.fromstr(jidparams['jid'])


async def main():
    client = aioxmpp.PresenceManagedClient(
        jid,
        aioxmpp.make_security_layer(jidparams['password']),
    )

    def message_response(msg):
        resp = msg.make_reply()
        resp.body[None] = 'you said: ' + msg.body.any()
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
