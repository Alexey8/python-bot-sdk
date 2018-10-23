from .service import ManagedService
from dialog_api import messaging_pb2, sequence_and_updates_pb2
from google.protobuf import empty_pb2
import time


class Messaging(ManagedService):
    def send_message(self, peer, text, interactive_media_groups=None):
        outpeer = self.manager.get_outpeer(peer)
        msg = messaging_pb2.MessageContent()
        msg.textMessage.text = text
        if interactive_media_groups is not None:
            for g in interactive_media_groups:
                media = msg.textMessage.media.add()
                g.render(media)
        return self.internal.messaging.SendMessage(messaging_pb2.RequestSendMessage(
            peer=outpeer,
            rid=int(time.time()),
            message=msg
        )).mid

    def on_message(self, callback):
        for update in self.internal.updates.SeqUpdates(empty_pb2.Empty()):
            up = sequence_and_updates_pb2.UpdateSeqUpdate()
            up.ParseFromString(update.update.value)
            if up.WhichOneof('update') == 'updateMessage':
                callback(up.updateMessage)