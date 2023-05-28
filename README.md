<div align="center">
  <p><img src="https://user-images.githubusercontent.com/91937041/235443858-85949be1-08d6-4d7a-b132-b1aed71ab943.png" width="560" alt="PoweredByNonebotLogo"></p>
  <a href="https://v2.nonebot.dev/store"><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-watermarker

_✨ 为你的bot发出的图片添加水印! ✨_

<a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">
    <img src="https://img.shields.io/github/license/forchannot/nonebot_plugin_rename" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-rename">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-rename.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-yellow.svg" alt="python">

</div>

<!-- TOC -->
  * [📖简介](#简介)
  * [💿 安装方法](#安装方法)
  * [⚙️插件配置项](#插件配置项)
  * [🎉目前已实现的功能](#目前已实现的功能)
  * [💡待实现的功能](#待实现的功能)
  * [💣已知bug](#已知bug)
  * [🔥鸣谢](#鸣谢)
  * [💦其他](#其他)
<!-- TOC -->

## 📖简介
为bot发出的所有图片都加上水印(有的时候水印很烦,但是帅气的水印能增加图片的美感,不是吗?)

## 💿安装方法
### ```nb脚手架```
<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```cmd
nb plugin install nonebot-piugin-watermarker
```

</details>

### ```pip```
<details>
<summary>pip安装</summary>

命令行输入以下命令

```cmd
pip install nonebot-plugin-watermarker
```

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_rename"]

```
[tool.nonebot]
plugins = []
plugin_dirs = ["src/plugins"]
```
</details>

##  ⚙插件配置项

| 变量名      |       变量类型    |   变量概述       |
|------------|----------------------------------|----------------|
| ```watermark_image_path```   |```str```|水印图片存放目录,目录下的所有水印图片会被随机选取|
| ```watermark_image_size```   |```float```|水印相对图片的大小(保持水印原来的形状)|
| ```watermark_image_exculed_plugin```   |```List[str]```|不想被贴水印的插件(未完工)|

## 🎉目前已实现的功能

### 加水印捏
<details>
<summary>效果图</summary>

![6PHLH{(JH $R~J2H@8{{XBE](https://user-images.githubusercontent.com/91937041/235442049-67ac0b4c-1629-4d78-9858-8b411b7ebe7b.jpg)

太小了看不见放大看(

![G37PR_ KAWEUINI_ _B)H2E](https://user-images.githubusercontent.com/91937041/235442112-c35e08ed-64c4-4b09-93f6-5976bb70de60.jpg)

</details>

## 💡待实现的功能

1. -[ ] 对特定的插件的图片不进行贴水印操作
2. -[ ] 待补充.....

# 💣已知bug

水印小概率贴不上,应该是base64的原因,但是我一直找不到真正的问题源,因为有时候贴的上有时候贴不上(已解决,base64解码问题,为末位不足位没有补上=)

# 🔥鸣谢

[Nonebot2](https://github.com/nonebot/nonebot2),不用说,没有Nonebot就没有这个插件

~~[我自己](https://github.com/X-Skirt-X),因为我做的PoweredByNonebot的Logo~~

# 💦其他

没有其他,想到再补
