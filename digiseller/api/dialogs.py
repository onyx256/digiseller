from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

from pydantic import BaseModel

from digiseller.api import ApiCategoryBase


class Message(BaseModel):
    class MessageFrom(Enum):
        SELLER = 'seller'
        BUYER = 'buyer'

    id: int
    text: Optional[str]
    deleted: bool

    date_written: datetime
    date_seen: datetime


class Dialog(BaseModel):
    """
    Представляет информацию о диалоге
    https://my.digiseller.com/inside/api_debates.asp#get_chats
    """

    class DialogState(Enum):
        UNKNOWN = -1
        CLOSED = 0
        OPEN_BY_SELLER = 1
        OPEN_BY_ADMIN = 2

    digiseller: object

    order_id: int
    email: str
    product_name: str
    last_date: datetime
    messages_count: int
    new_messages_count: int

    def get_status(self) -> Dict:
        state = self.digiseller.dialogs.get_status(self.order_id)
        return state

    def change_status(self, closed: bool) -> bool:
        result = self.digiseller.dialogs.change_status(order_id=self.order_id,
                                                       closed=closed)
        return result

    def get_messages(self, limit: int = 20) -> List[Message]:
        messages = self.digiseller.dialogs.get_messages(limit)
        return messages


class Dialogs(ApiCategoryBase):
    def __init__(self, digiseller: object) -> None:
        super().__init__(digiseller)

    def get_all(self,
                limit: int = 20) -> List[Dialog]:
        if limit == 0:
            limit = 9999

        current_page = 1

        dialogs = []
        while True:
            resp = self.digiseller.make_request(
                'get', 'debates/v2/chats',
                filter_new=0,
                email=None,
                id_ids=None,
                pagesize=limit if limit < 200 else 200,
                page=current_page
            )
            data = resp.json()
            pages_count: int = data['pages']

            _dialogs = data['chats']
            for dialog in _dialogs:
                if len(dialogs) >= limit:
                    break

                dialogs.append(
                    Dialog(
                        digiseller=self.digiseller,
                        order_id=dialog['id_i'],
                        email=dialog['email'],
                        product_name=dialog['product'],
                        last_date=datetime.fromisoformat(dialog['last_date']),
                        messages_count=dialog['cnt_msg'],
                        new_messages_count=dialog['cnt_new']
                    )
                )

            if current_page >= pages_count:
                break
            else:
                current_page += 1

        return dialogs

    def get_status(self,
                   order_id: int):
        resp = self.digiseller.make_request(
            'get', 'debates/v2/chat-state',
            id_i=order_id
        )
        data = resp.json()

        dialog_state = Dialog.DialogState(data['chat_state'])
        may_change = data['may_change']

        return {
            'state': dialog_state,
            'may_change': bool(may_change)
        }

    def change_status(self,
                      order_id: int,
                      closed: bool) -> bool:
        resp = self.digiseller.make_request(
            'post', 'debates/v2/chat-state',
            use_json=False,
            raise_for_status=False,
            id_i=order_id,
            chat_state=0 if closed else 1
        )
        if resp.status_code == 200:
            return True
        else:
            return False

    def get_messages(self,
                     order_id: int,
                     limit: int = 20):
        # у ключа нет прав, че за залупа?
        raise NotImplementedError

        if limit == 0:
            limit = 9999

        messages = []
        while True:
            resp = self.digiseller.make_request(
                'get', 'debates/v2',
                id_i=order_id,
                hidden=0,
                count=limit if limit < 200 else 200
            )
            data = resp.json()
            _messages = data
            if not _messages:
                break

            for message in _messages:
                messages.append(
                    Message(
                        id=message['id'],
                        text=message.get('message'),
                        deleted=bool(message['deleted']),
                        date_written=datetime.fromisoformat(message['date_written']),
                        date_seen=datetime.fromisoformat(message['date_seen']),
                    )
                )

            break

        return messages
