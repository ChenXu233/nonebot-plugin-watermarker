import os
from pathlib import Path
from pydantic import BaseModel, Extra
from typing import Union, Tuple, Iterable, Literal

from nonebot import get_driver

driver = get_driver()


class Config(BaseModel, extra=Extra.ignore):
    watermark_image_path: Path = (
        Path(os.path.dirname(__file__)) / "watermarker_image"
    )  # 水印图片存放目录,目录下的所有水印图片会被随机选取
    watermark_image_size: float = 0.07  # 水印相对图片的大小(保持水印原来的形状)
    watermark_image_exculed_plugin: Iterable[str] = []  # TODO: 增加对特定插件的排除
    # watermark_image_position: Union[
    #     Literal["左上", "右上", "左下", "右下", "居中"], Tuple[int, int] #以后再说,先 TODO 了
    # ] = "右下"


config = Config.parse_obj(driver.config.dict())
