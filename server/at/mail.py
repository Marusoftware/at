from asyncio import Queue
from email.message import EmailMessage
import aiosmtplib
from .config import Settings

config=Settings()
class MailController():
    msgQueue:Queue[EmailMessage]
    def __init__(self):
        self.msgQueue = Queue()
    async def addMessage(self, message:EmailMessage):
        await self.msgQueue.put(message)
    async def _sendloop(self):
        while True:
            message=await self.msgQueue.get()
            try:
                await aiosmtplib.send(message, hostname=config.MAIL_SERVER, **config.MAIL_OPTIONS)
            except:
                import traceback
                print("error: ", traceback.format_exc(), flush=True)
    async def shutdown(self):
        pass
mail=MailController()