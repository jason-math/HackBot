import asyncio


# Voice channel that times out
class PrivateRoom:
    active_check = True
    private_channel = None

    async def assign_channel(self, channel):
        self.private_channel = channel

    async def active_checker(self):
        if len(self.private_channel.members) == 0:
            if self.active_check is True:
                self.active_check = False
            else:
                await self.private_channel.delete()
                self.private_channel = None
                return
        else:
            self.active_check = True
        await asyncio.sleep(600)
