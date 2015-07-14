from pytg import Telegram
from pytg.utils import coroutine


tg = Telegram(telegram="/usr/bin/telegram-cli", pubkey_file="/etc/telegram-cli/server.pub", port=9918)
receiver = tg.receiver
sender = tg.sender

MYID = 92432906  # user id for farseerfc
GROUPS = [(9615403, "Arch2", "arch2.jpg")]


@coroutine  # from pytg.utils import coroutine
def main_loop():
    while True:
        msg = (yield)  # it waits until it got a message, stored now in msg.
        for grp in GROUPS:
            grpid, grpname, grpphoto = grp
            if msg.event == "updates" and all(["title" in msg["updates"],
                    msg.peer["id"] == grpid, msg.peer["title"] != grpname]):
                sender.raw("rename_chat " + msg.peer["title"] + " " + grpname)
                print("----Changed to " + grpname + " --")
            if msg.event == "service" and all(["chat_change_photo" in msg.action["type"],
                    msg.receiver["id"] == grpid, msg.sender["id"] != MYID]):
                sender.raw("chat_set_photo " + msg.peer["title"] + " " + grpphoto)
                print("----Changed Photo to " + grpname + " --")
        print("Message: ", msg)

receiver.start()
receiver.message(main_loop())
