import io
import re
import os
import base64
import random
import urllib.request
from PIL import Image, ImageFont, ImageDraw, ImageSequence

from pathlib import Path
from typing import Union, List, Tuple

from nonebot.log import logger

from .config import config


async def str2img(string: str) -> Union[Image.Image, None]:
    """传入的MessageSegment中的file的字符串转换为PIL图片对象

    Args:
        string (str): _description_

    Returns:
        Union[Image.Image, None]: _description_
    """
    base64_pattern = r"base64://[a-zA-Z0-9+/]+"
    other_pattern = r"(?:http|https)://\S+"
    file_pattern = r"file:///\S+"
    image1 = None
    #breakpoint()
    if matcher := re.search(base64_pattern, string):
        string = matcher.group()
        string = string.replace("base64://", "")
        if base64_miss_padding := (4 - len(string) % 4):
            string += "=" * base64_miss_padding
        image_bytes = base64.b64decode(string)
        image_stream = io.BytesIO(image_bytes)
        image1 = Image.open(image_stream)
    elif matcher := re.search(other_pattern, string):
        string = matcher.group()
        image_bytes = urllib.request.urlopen(string).read()
        image_stream = io.BytesIO(image_bytes)
        image1 = Image.open(image_stream)
    elif matcher := re.search(file_pattern, string):
        string = matcher.group()
        image_bytes = urllib.request.urlopen(string).read()
        image_stream = io.BytesIO(image_bytes)
        image1 = Image.open(image_stream)

    return image1


def get_image_dirs(path: Union[str, Path]) -> List[str]:
    """获得传入目录下的所有图片(AI写的,错了不怪我())

    Args:
        path (Union[str, Path]): 查询的目录

    Returns:
        List[str]: 包含所有返回的图片目录
    """
    # 定义一个空列表，用来存储图片目录
    image_dirs = []
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(path):
        # 遍历文件
        for file in files:
            # 判断文件是否是图片类型
            if file.endswith((".jpg", ".png")):
                # 获取文件的绝对路径
                image_path = os.path.join(root, file)
                # 将图片目录添加到列表中
                image_dirs.append(image_path)
    # 返回图片目录列表
    return image_dirs


def position(image: Image.Image, watermark: Image.Image, where: Tuple[int, int]):
    """TODO:不知道要不要做这个抽象"""
    pass

async def watermark_on_jpg(image:Image.Image) -> str:
    image_size = image.size
    watermark_path = random.choice(get_image_dirs(config.watermark_image_path))
    watermark = Image.open(watermark_path)
    mix = tuple([int((k + j) / 2) for k, j in zip(watermark.size, image_size)])
    watermark_size = tuple([int(k * config.watermark_image_size) for k in mix])
    watermark_position = tuple(
        [k - j for k, j in zip(image_size, watermark_size)]
    )
    watermark.thumbnail(watermark_size)
    logger.debug(f"watermark_size:{watermark_size}\nimage_size:{image_size}")
    image = image.convert("RGBA")
    watermark = watermark.convert("RGBA")
    mask = watermark.split()[3]

    image.paste(watermark, watermark_position, mask)

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    byte_data = buffered.getvalue()
    return base64.b64encode(byte_data).decode("utf-8")