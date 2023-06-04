from typing import Dict, Any
from dataclasses import asdict

from nonebot import on_command
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.matcher import Matcher
from nonebot.adapters import Bot,Event,Message
from nonebot.permission import SUPERUSER
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

watermark_switch = on_command(
    cmd='水印',
    aliases=set({'watermarker','水印大师'}),
    priority=2,
    permission=SUPERUSER
)

@watermark_switch.handle()
async def _switch_handle(matcher:Matcher,bot:Bot,Event:Event,args:Message=CommandArg()):
    #TODO: 不知道为什么,以下方法均不能使用
    args:List[str] = args.extract_plain_text().strip().split(' ')
    if 'on' in args or '打开' in args:
        config.watermark_switch = True
    elif 'off' in args or '关闭' in args:
        config.watermark_switch = False
    if 'add' in args or '添加' in args:
        try:
            args.remove('add')
        except ValueError:
            args.remove('添加')
        config.watermark_image_exculed_plugin.extend(args)
    elif 'del' in args and "删除" in args:
        try:
            args.remove('del')
        except ValueError:
            args.remove('删除')
        err_args = []
        for i in args:
            try:
                config.watermark_image_exculed_plugin.remove(i)
            except ValueError:
                err_args.append(i)
        matcher.finish(f'删除以下配置发送错误:\n{err_args}\n这些名称不在插件黑名单中')

@Bot.on_calling_api
async def _handle(bot: Bot, api: str, data: Dict[str, Any]):
    if not config.watermark_switch:
        return
    if api not in ["send_msg", "send_message"]:
        return
    if i := current_matcher.get().module_name:
        if i in config.watermark_image_exculed_plugin:
            return

    logger.info(
        "handling message form module={}\
        \n如果你不想给这个插件加水印,请在配置里写入这里输出的module名称(注意!不要把module=给带上了!)"\
        .format(current_matcher.get().module_name)
        )
    for i in range(len(data["message"])):
        image_data = asdict(data["message"][i])
        if image_data["type"] != "image":continue
        #有减少嵌套的方法记得踹我
        if image := await str2img(image_data["data"]["file"]):
            if image.format == 'GIF':
                base64_str = watermark_on_gif(image)
            else:
                base64_str = watermark_on_jpg(image)
            data["message"][i].data["file"] = "base64://" + base64_str

        else:
            logger.debug("这是一个代表图片的东西吗???:\n"+image_data["data"]["file"][:50])
