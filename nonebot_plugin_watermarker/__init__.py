import base64
import random

from PIL import Image
from io import BytesIO
from typing import Dict, Any
from dataclasses import asdict
from contextvars import copy_context

from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Bot

from .config import *
from .fuctions import *

image_dirs = get_image_dirs(config.watermark_image_path)

__plugin_meta__ = PluginMetadata(
    name="图片水印",
    description="为bot发出的图片添加水印",
    usage="用来给bot发出的图片添加水印",
    config=Config,
)


@Bot.on_calling_api
async def _handle(bot: Bot, api: str, data: Dict[str, Any]):
    if api not in ["send_msg", "send_message"]:
        return
    logger.debug("handle start")
    for i in range(len(data["message"])):
        image_data = asdict(data["message"][i])
        if image_data["type"] != "image":
            continue
        file = image_data["data"]["file"]
        if image := await str2img(file):
            image_size = image.size
            watermark_path = random.choice(image_dirs)
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

            buffered = BytesIO()
            image.save(buffered, format="PNG")
            byte_data = buffered.getvalue()
            base64_str = base64.b64encode(byte_data).decode("utf-8")
            data["message"][i].data["file"] = "base64://" + base64_str

        else:
            logger.debug(file)
