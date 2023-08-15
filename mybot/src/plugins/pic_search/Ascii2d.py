from typing import Optional
from PicImageSearch import Ascii2D, Network
from PicImageSearch.model import Ascii2DItem

from utils.CardMessage import CardMessage


class Ascii2d:
    @staticmethod
    async def get_resp(
        image_url: str, proxies: Optional[str] = None, verify_ssl: bool = True
    ):
        async with Network(proxies=proxies, verify_ssl=verify_ssl) as client:
            ascii2d_normal = Ascii2D(client=client)
            ascii2d_bovm = Ascii2D(client=client, bovw=True)
            resp_nomal = await ascii2d_normal.search(url=image_url)
            resp_bovm = await ascii2d_bovm.search(url=image_url)
            selected_normal = next(
                (i for i in resp_nomal.raw if i.title or i.url_list), resp_nomal.raw[0]
            )
            selected_bovm = next(
                (i for i in resp_bovm.raw if i.title or i.url_list), resp_bovm.raw[0]
            )
            return [selected_normal, selected_bovm]

    @staticmethod
    def norlmal_card(resp: Ascii2DItem):
        new_card = CardMessage()
        new_card.add_plain_text("Ascii2dse色合搜索:")
        new_card.add_plain_text(f"{resp.title} / {resp.author}")
        new_card.add_image(resp.thumbnail)
        new_card.add_kmarkdown(f"url: [{resp.url}]({resp.url})")
        new_card.add_kmarkdown(f"author: [{resp.author_url}]({resp.author_url})")
        return new_card.card

    @staticmethod
    def bovm_card(resp: Ascii2DItem):
        new_card = CardMessage()
        new_card.add_plain_text("Ascii2dse特征搜索:")
        new_card.add_plain_text(f"{resp.title} / {resp.author}")
        new_card.add_image(resp.thumbnail)
        new_card.add_kmarkdown(f"url: [{resp.url}]({resp.url})")
        new_card.add_kmarkdown(f"author: [{resp.author_url}]({resp.author_url})")
        return new_card.card
