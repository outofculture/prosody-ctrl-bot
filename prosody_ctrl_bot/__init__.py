import asyncio
import re

import aioxmpp
import aioxmpp.dispatcher

from prosody_ctrl_bot.passwords import make_password

jidparams = {
    'jid': 'serverbot@outofinter.net',
    # 'password': 'fake',
}

my_jid = aioxmpp.JID.fromstr(jidparams['jid'])

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
