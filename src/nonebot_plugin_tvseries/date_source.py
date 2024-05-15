from pathlib import Path
from typing import Optional

from lxml import etree
from nonebot import require
from nonebot.adapters import Bot
from nonebot.drivers import Request
import datetime

new_page = require("nonebot_plugin_htmlrender").get_new_page


async def get_tvseries(bot: Bot, week: Optional[str] = None) -> bytes:
    url = "https://huo720.com/calendar"

    # if week:
    #     url += f"?{parse_week(week)}"
    req = Request("GET", url)
    res = await bot.adapter.request(req)
    result = parse_data(str(res.content))
    image = await create_image(result)
    return image


def parse_date(date: Optional[str] = None) -> str:


    now = datetime.datetime.now()
    return now.strftime(r"%Y-%m-%d")


def parse_data(content: str) -> str:
    css = Path(__file__).parent / "css.css"
    with css.open("r") as f:
        css = f.read()

    dom = etree.HTML(content)
    result = dom.xpath(f'//*[@id="{parse_date()}"]')[0]

    html_init = f"""<html><head><meta charset="utf-8"><style type="text/css">{css}</style></head><body><div id="main-container"></div></body></html>"""
    new_dom = etree.HTML(html_init)
    container = new_dom.xpath("//body/div")[0]

    container.append(result)
    html = etree.tostring(new_dom, encoding="utf-8", method="html").decode()

    return html


async def create_image(html: str, wait: int = 0) -> bytes:
    async with new_page(viewport={"width": 1200, "height": 600}) as page:
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(wait)
        img_raw = await page.screenshot(full_page=True)
    return img_raw
