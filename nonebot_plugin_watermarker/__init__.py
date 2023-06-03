from typing import Dict, Any
from dataclasses import asdict

from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Bot
from nonebot.internal.matcher import current_matcher
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
    if i := current_matcher.get().module_name:
        if i in config.watermark_image_exculed_plugin:
            return

    logger.debug("handle start")
    for i in range(len(data["message"])):
        image_data = asdict(data["message"][i])
        if image_data["type"] != "image":continue

        if image := await str2img(image_data["data"]["file"]):
            if image.format == 'GIF':return #暂时对GIF没有适配
            else:
                data["message"][i].data["file"] = "base64://" + (await watermark_on_jpg(image))

        else:
            logger.debug("这是一个代表图片的东西吗???:\n"+image_data["data"]["file"][:50])

