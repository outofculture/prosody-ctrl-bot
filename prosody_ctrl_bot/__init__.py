import asyncio
import io
import re
import subprocess

import aioxmpp
import aioxmpp.dispatcher

from prosody_ctrl_bot.config import jidparams, my_jid
from prosody_ctrl_bot.passwords import make_password


DEVICELIST_NODE = 'eu.siacs.conversations.axolotl.devicelist'
FAILURE_MESSAGE = 'I failed at the one thing you asked of me -_-'
BAD_CHARS = '[^-@_ ./0-9a-zA-Z]'


def execute_prosody(command: str, *interactive_responses: str) -> bool:
    command = 'prosodyctl {}'.format(command)
    has_bad_chars = re.search(BAD_CHARS, command)
    if has_bad_chars or len(command) > 1023:
        # super paranoid whitelist
        print('unsafe command detected: "{}" ({})'.format(command, has_bad_chars.group()))
        return False
    else:
        print('executing prosody command {}'.format(command))
        proc = subprocess.Popen(
            command.split(' '),
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        stdin = io.TextIOWrapper(
            proc.stdin,
            encoding='utf-8',
        )
        for input_str in interactive_responses:
            stdin.write('{}\n'.format(input_str))
        stdin.flush()
        print(proc.communicate()[0].decode('utf-8'))
        proc.wait()
        if proc.returncode != 0:
            print('process failed')
            print(proc.returncode)
            return False
        else:
            print('prosodyctl command succeeded')
            return True


async def main():
    client = aioxmpp.PresenceManagedClient(
        my_jid,
        aioxmpp.make_security_layer(jidparams['password']),
    )

    def handle_direct_message(msg):
        if not msg.body:
            return
        resp = msg.make_reply()
        command = msg.body.any()
        if command.lower().startswith('password'):
            new_password = command[len('password '):].strip()
            if not new_password:
                resp.body[None] = 'Missing required information. Usage: "password [NEW PASSWORD]" ( trailing whitespace is ignored )'
            else:
                # TODO strip client info from from_ jid
                successful = execute_prosody(
                    'passwd {}'.format(msg.from_),
                    new_password,
                    new_password,
                )
                if successful:
                    resp.body[None] = 'Password changed to "{}"'.format(new_password)
                else:
                    resp.body[None] = FAILURE_MESSAGE
        elif command.lower().startswith('new user'):
            username = command[len('new user '):].strip().lower()
            if not username:
                resp.body[None] = 'Missing required information. Usage: "new user [USERNAME]"'
            else:
                password = make_password()
                successful = execute_prosody(
                    'adduser {}@{}'.format(username, my_jid.domain),
                    password,
                    password,
                )
                if successful:
                    resp.body[None] = 'User {}@outofinter.net created. Tell them that their password is "{}"'.format(
                        username, password)
                else:
                    resp.body[None] = FAILURE_MESSAGE
        else:
            resp.body[None] = 'I have no idea how to respond to that o_O'

        client.enqueue(resp)

    dispatch = client.summon(aioxmpp.dispatcher.SimpleMessageDispatcher)
    dispatch.register_callback(
        aioxmpp.MessageType.CHAT,
        None,
        handle_direct_message,
    )

    client.summon(aioxmpp.EntityCapsService)  # prereq for PEP
    pep = client.summon(aioxmpp.PEPClient)
    claim = pep.claim_pep_node(
        DEVICELIST_NODE,
        notify=True,
    )
    # TODO claim.publish(some_data_to_say_i_have_a_device)
    # TODO make sure my device is in my device list
    # TODO initialize omemo

    def handle_devicelist_update(jid, node, item, message=None):
        buf = io.BytesIO()
        aioxmpp.xml.write_single_xso(item, buf)
        # TODO unpack the devicelist from the item
        # TODO put the device ids into the omemo store
        # sessionMgr.newDeviceList(devices, jid)

        print(jid, node, buf.getvalue().decode("utf-8"))

    claim.on_item_publish.connect(handle_devicelist_update)

    async with client.connected():
        while True:
            await asyncio.sleep(1)
