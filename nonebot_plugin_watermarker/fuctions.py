import io
import re
import os
import base64
import urllib.request
import PIL.Image as Image

from pathlib import Path
from typing import Union, List, Tuple


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
    breakpoint()
    if matcher := re.search(base64_pattern, string):
        string = matcher.group()
        string = string.replace("base64://", "")
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
