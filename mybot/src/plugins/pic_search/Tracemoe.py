from typing import Optional
from PicImageSearch import Network, TraceMoe
from PicImageSearch.model import TraceMoeResponse

from utils.CardMessage import CardMessage


class Tracemoe:
    @staticmethod
    async def get_resp(
        img_url: str,
        proxies: Optional[str] = None,
        mute: bool = False,
        size: Optional[str] = None,
    ):
        async with Network(proxies=proxies) as client:
            tracemoe = TraceMoe(client=client, mute=mute, size=size)
            resp = await tracemoe.search(url=img_url)
            return resp

    @staticmethod
    def generate_card(resp: TraceMoeResponse):
        def convert_to_time_format(float_num):
            minutes = int(float_num // 60)  # 取整数部分作为分钟数
            seconds = int(float_num % 60)  # 取余数部分作为秒数
            return f"{minutes}:{seconds:02}"

        new_card = CardMessage()
        new_card.add_plain_text(
            f"[{resp.raw[0].similarity}%] {resp.raw[0].title_native}"
        )
        new_card.add_plain_text(f"译名: {resp.raw[0].title_chinese}")
        new_card.add_image(resp.raw[0].cover_image)
        new_card.add_plain_text(
            f"上映时间: {resp.raw[0].start_date['year']}-{resp.raw[0].start_date['month']}-{resp.raw[0].start_date['day']}"
        )
        new_card.add_plain_text(
            f"下映时间: {resp.raw[0].end_date['year']}-{resp.raw[0].end_date['month']}-{resp.raw[0].end_date['day']}"
        )
        new_card.add_plain_text(f"Episode: {resp.raw[0].episode}")
        new_card.add_plain_text(
            f"进度: {convert_to_time_format(resp.raw[0].From)}-{convert_to_time_format(resp.raw[0].To)}"
        )
        new_card.add_video(title=resp.raw[0].filename, src=resp.raw[0].video)
        return new_card
