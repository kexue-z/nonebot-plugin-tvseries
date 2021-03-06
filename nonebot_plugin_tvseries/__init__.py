from .date_source import get_tvseries
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment


tvseries = on_command("剧集", aliases={"tvseries"})


@tvseries.handle()
async def _(bot: Bot, event: MessageEvent):
    pic_bytes = await get_tvseries()
    await tvseries.finish(MessageSegment.image(pic_bytes))
