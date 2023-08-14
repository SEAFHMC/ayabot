from nonebot.plugin import on_command
from nonebot.adapters.kaiheila.message import MessageSegment
from nonebot.adapters.kaiheila import Bot
from httpx import AsyncClient

cmd = on_command("来份涩图", aliases={"来份色图", "来份瑟图"})


@cmd.handle()
async def _(bot: Bot):
    async with AsyncClient() as client:
        resp = await client.get("瑟图网站")
    file_key = await bot.upload_file(resp.content)
    await cmd.finish(MessageSegment.image(file_key=file_key))
