from nonebot import on_command, require
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .date_source import get_tvseries

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage

__plugin_meta__ = PluginMetadata(
    name="获取美剧",
    description="通过火720网站获取美剧信息",
    usage="剧集",
    homepage="https://github.com/kexue-z/nonebot-plugin-tvseries",
    type="application",
    config=None,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "author": "kexue",
        "priority": 1,
        "version": "0.0.2.3",
    },
)


tvseries = on_command("剧集", aliases={"tvseries"})


@tvseries.handle()
async def _(bot: Bot):
    pic_bytes = await get_tvseries(bot=bot)
    await UniMessage.image(raw=pic_bytes).finish()
