from loguru import logger

from PicImageSearch.model import SauceNAOResponse
from PicImageSearch.sync import SauceNAO as SauceNAOSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
api_key = ""


@logger.catch()
def test_sync() -> None:
    saucenao = SauceNAOSync(proxies=proxies, api_key=api_key, hide=3)
    resp = saucenao.search(url=url)
    show_result(resp)  # type: ignore


def show_result(resp: SauceNAOResponse) -> None:
    logger.info(resp.status_code)  # HTTP 状态码
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].similarity)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].author)
    logger.info(resp.raw[0].author_url)
    logger.info(resp.raw[0].url)
    logger.info("-" * 50)


if __name__ == "__main__":
    test_sync()
