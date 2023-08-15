from loguru import logger
from typing import Optional
from PicImageSearch import Ascii2D, Network
from PicImageSearch.model import Ascii2DResponse
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
            return {"normal": resp_nomal, "bovm": resp_bovm}

    @staticmethod
    def generate_card(resp: Ascii2DResponse):
        pass


def show_result(resp: Ascii2DResponse) -> None:
    selected = next((i for i in resp.raw if i.title or i.url_list), resp.raw[0])
    logger.info(selected.thumbnail)
    logger.info(selected.title)
    logger.info(selected.author)
    logger.info(selected.author_url)
    logger.info(selected.url)
    logger.info("-" * 50)
