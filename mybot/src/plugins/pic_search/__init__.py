import nonebot

from nonebot.typing import T_State
from nonebot.plugin import on_fullmatch
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.adapters.kaiheila.message import Message, MessageSegment

from .SauceNao import SauceNao
from .Ascii2d import Ascii2d
from .Tracemoe import Tracemoe
from .config import Config, ConfigError

plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if not plugin_config.saucenao_key:
    raise ConfigError("请设置 saucenao_key")
pic_search = on_fullmatch("文文搜图")


@pic_search.handle()
async def _(matcher: Matcher, state: T_State, arg: Message = CommandArg()):
    state["search_mode"] = "saucenao"
    if arg.extract_plain_text():
        matcher.set_arg("msg_recv", arg)


@pic_search.got("msg_recv", prompt="了解～请发送图片吧！支持批量噢！\n如想退出搜索模式请发送“谢谢文文”")
async def got_arg(state: T_State, msg_recv: Message = Arg()):
    # 文字参数处理
    if msg_recv[0].type == "text":
        arg_plain_text = msg_recv.extract_plain_text()
        if arg_plain_text == "谢谢文文":
            await pic_search.finish("にゃ～")
        if arg_plain_text not in ["saucenao", "anime", "a2d"]:
            await pic_search.reject("必须要发送图片我才能帮你找噢_(:3」」\n支持批量！")
        state["search_mode"] = arg_plain_text
        await pic_search.reject(f"了解～已进入{arg_plain_text}搜图模式")
    # 图片参数处理
    elif msg_recv[0].type == "image":
        file_key = msg_recv[0].data["file_key"]
        # SauceNao
        if state["search_mode"] == "saucenao":
            resp = await SauceNao.get_resp(img_url=file_key, api_key=plugin_config.saucenao_key)  # type: ignore
            await pic_search.send(
                MessageSegment.Card(SauceNao.generate_card(resp=resp))
            )
            if resp.raw[0].similarity < 60:
                await pic_search.send(
                    f"相似度 {resp.raw[0].similarity}% 过低，如果这不是你要找的图，那么可能：确实找不到此图/图为原图的局部图/图清晰度太低/搜索引擎尚未同步新图\n自动使用 ascii2d 进行搜索"
                )
                resps = await Ascii2d.get_resp(image_url=file_key)
                await pic_search.send(
                    MessageSegment.Card(Ascii2d.norlmal_card(resp=resps[0]))
                )
                await pic_search.reject(
                    MessageSegment.Card(Ascii2d.bovm_card(resp=resps[1]))
                )
            await pic_search.reject()
        # Ascii2d
        if state["search_mode"] == "a2d":
            resps = await Ascii2d.get_resp(image_url=file_key)
            await pic_search.send(
                MessageSegment.Card(Ascii2d.norlmal_card(resp=resps[0]))
            )
            await pic_search.reject(
                MessageSegment.Card(Ascii2d.bovm_card(resp=resps[1]))
            )
        # Anime
        if state["search_mode"] == "anime":
            resp = await Tracemoe.get_resp(img_url=file_key)
            await pic_search.reject(
                MessageSegment.Card(Tracemoe.generate_card(resp=resp))
            )
    # Default
    else:
        await pic_search.reject("必须要发送图片我才能帮你找噢_(:3」」\n支持批量！")
