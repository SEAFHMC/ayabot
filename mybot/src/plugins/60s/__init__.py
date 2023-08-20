from nonebot.plugin import on_command
from nonebot.adapters.kaiheila.message import MessageSegment
from httpx import AsyncClient

from utils.CardMessage import CardMessage


sixty_secs = on_command("60s")


@sixty_secs.handle()
async def _():
    async with AsyncClient() as client:
        resp = await client.get("https://api.2xb.cn/zaob")
    img_url = resp.json()["imageUrl"]
    new_card = CardMessage()
    new_card.add_image(img_url)
    await sixty_secs.finish(MessageSegment.Card(new_card.card))
