import re, requests
from astrbot.api.all import Star, Context, register
from astrbot.api.event import CommandResult, AstrMessageEvent
from bilibili_api import video, Credential
from astrbot.api.message_components import Image, Plain
from astrbot.api.event.filter import regex

# 正则匹配
BV = (
    r"(?:"
    r".*?(?:https?://)?(?:www\.|m\.)?bilibili\.com/(?:video/)?"
    r"(?P<standard_bv>BV[a-zA-Z0-9]{10})(?:[/?].*?)?|"  # 标准/移动端链接（兼容无video路径）
    r".*?(?:https?://)?(?:bili2233.cn)/(?P<short_bv>BV[a-zA-Z0-9]{10})|"  # 短链接（兼容备用域名）
    r"(?<![\w/])(?P<raw_bv>BV[a-zA-Z0-9]{10})(?![\w/])"  # 独立BV号（严格边界检测）
    r")"
)


SHORT_LINK = (
    r"(?:"
        r".*?(?:https?://)?(b23\.tv)/(?P<short_bv>[a-zA-Z0-9]{7})"
    r")"
)

SHORT_LINK_PATTERN = r"(https?://)?(b23\.tv)/(?P<short_bv>[a-zA-Z0-9]{7})"


@register("astrbot_plugin_bilipic_x", "unkoe", "发送BV号获取哔站视频封面图", "1.0", "https://github.com/unkoe/bilipic")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.context = context

    @regex(BV)
    async def get_video_info(self, message: AstrMessageEvent):
        if len(message.message_str) == 12:
            bvid = message.message_str
        else:
            match_ = re.search(BV, message.message_str, re.IGNORECASE)
            if not match_:
                return
            bvid = "BV" + match_.group(1)[2:]

        v = video.Video(bvid=bvid,)
        info = await v.get_info()
        
        # 合并文本和图片一起发送
        message_content = [
            Plain(f"""📺 bilibili 视频信息：
            标题：{info['title']}
            博主：{info['owner']['name']}
            播放：{info['stat']['view']} | 点赞：{info['stat']['like']} | 投币：{info['stat']['coin']}"""),
            Image.fromURL(info["pic"])
        ]
        
        return CommandResult(chain=message_content).use_t2i(False)
        
    

    @regex(SHORT_LINK)
    async def get_video_info_shortlink(self, message: AstrMessageEvent):
        match_ = re.search(SHORT_LINK_PATTERN, message.message_str, re.IGNORECASE)
        if not match_:
            return
        short_url = match_.group()
        if short_url:
            response = requests.get(short_url, allow_redirects=False)
            real_url = response.headers['Location']
            match_ = re.search(BV, real_url, re.IGNORECASE)
            if not match_:
                return
            bvid = "BV" + match_.group(1)[2:]
        v = video.Video(bvid=bvid,)
        info = await v.get_info()
        
        # 合并文本和图片一起发送
        message_content = [
            Plain(f"""📺 bilibili 视频信息：
            标题：{info['title']}
            博主：{info['owner']['name']}
            播放：{info['stat']['view']} | 点赞：{info['stat']['like']} | 投币：{info['stat']['coin']}"""),
            Image.fromURL(info["pic"])
        ]
        
        return CommandResult(chain=message_content).use_t2i(False)
