"""
MIT License

Copyright (c) 2022 Aʙɪsʜɴᴏɪ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import threading

from sqlalchemy import Column, String

from Exon.modules.sql import BASE, SESSION


class FallenChats(BASE):
    __tablename__ = "fallen_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

FallenChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_fallen(chat_id):
    try:
        chat = SESSION.query(FallenChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def set_fallen(chat_id):
    with INSERTION_LOCK:
        fallenchat = SESSION.query(FallenChats).get(str(chat_id))
        if not fallenchat:
            fallenchat = FallenChats(str(chat_id))
        SESSION.add(fallenchat)
        SESSION.commit()

def rem_fallen(chat_id):
    with INSERTION_LOCK:
        fallenchat = SESSION.query(FallenChats).get(str(chat_id))
        if fallenchat:
            SESSION.delete(fallenchat)
        SESSION.commit()
