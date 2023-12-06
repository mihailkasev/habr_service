from urllib import parse

from core.settings import HABR


def create_link(link: str) -> str:
    """
    Создает абсолютную ссылку из относительной
    :param link Относительная ссылка
    :return Абсолютная ссылка
    """
    return parse.urljoin(HABR, link)
