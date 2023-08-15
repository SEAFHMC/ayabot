from typing import Optional
from PicImageSearch.model import SauceNAOResponse
from PicImageSearch import Network, SauceNAO

from utils import CardMessage


class SauceNao:
    @staticmethod
    async def get_resp(
        img_url: str, api_key: str, hide: int = 0, proxies: Optional[str] = None
    ):
        async with Network(proxies=proxies) as client:
            saucenao = SauceNAO(client=client, api_key=api_key, hide=hide)
            resp = await saucenao.search(url=img_url)
            return resp

    @staticmethod
    def generate_card(resp: SauceNAOResponse):
        new_card = CardMessage()
        new_card.add_plain_text(
            f"[{resp.raw[0].similarity}%] 「{resp.raw[0].title}」 / 「{resp.raw[0].author}」"
        )
        new_card.add_image(resp.raw[0].thumbnail)
        new_card.add_kmarkdown(f"illustration: [{resp.raw[0].url}]({resp.raw[0].url})")
        new_card.add_kmarkdown(
            f"author: [{resp.raw[0].author_url}]({resp.raw[0].author_url})"
        )
        return new_card.card
