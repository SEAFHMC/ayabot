import nonebot

from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.adapters.kaiheila.message import Message, MessageSegment

from .SauceNao import SauceNao
from .config import Config, ConfigError

plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if not plugin_config.saucenao_key:
    raise ConfigError("请设置 saucenao_key")
pic_search = on_command("搜图")


@pic_search.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    if arg.extract_plain_text():
        matcher.set_arg("msg_recv", arg)


@pic_search.got("msg_recv", prompt="请发送一张图片或者搜图模式")
async def got_arg(state: T_State, msg_recv: Message = Arg()):
    state["search_mode"] = "saucenao"
    # 文字参数处理
    if msg_recv[0].type == "text":
        arg_plain_text = msg_recv.extract_plain_text()
        if arg_plain_text == "退出":
            await pic_search.finish("已退出搜图")
        if arg_plain_text not in ["saucenao", "anime", "a2d"]:
            await pic_search.reject("参数不支持")
        state["search_mode"] = arg_plain_text
        await pic_search.reject(f"已进入{arg_plain_text}搜图模式")
    # 图片参数处理
    elif msg_recv[0].type == "image":
        file_key = msg_recv[0].data["file_key"]
        if state["search_mode"] == "saucenao":
            resp = await SauceNao.get_resp(img_url=file_key, api_key=plugin_config.saucenao_key)  # type: ignore
            await pic_search.finish(
                MessageSegment.Card(SauceNao.generate_card(resp=resp))
            )
    # Default
    else:
        await pic_search.finish("参数不支持")
