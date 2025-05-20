import re

# 正则表达式（注意末尾的 `|` 可能导致问题，建议删除或补全）
# pattern = r".*?(?:https?://)?(?:b23\.tv)/(?P<short_bv>[a-zA-Z0-9]{7})"
# pattern = r"(?:https?://)?(b23\.tv)/(?P<short_bv>[a-zA-Z0-9]{7})"
# pattern = r"https?://b23\.tv?P<short_bv>[a-zA-Z0-9]{7}"
pattern = r"(https?://)?(b23\.tv)/(?P<short_bv>[a-zA-Z0-9]{7})"

# 编译正则表达式（添加 re.IGNORECASE 以忽略大小写）
regex = re.compile(pattern, re.IGNORECASE)

# 测试用例
test_cases = [
    # 合法案例
    # ("b23.tv/qZO8Jiw", True), # 基础连接
    ("https://b23.tv/qZO8Jiw", True), # 带协议头
    ("前缀https://b23.tv/qZO8Jiw", True), # 含前缀

    
    # 非法案例
    ("b23.tv/BV1A441v7e7", False),          # 过时基础短链
    ("https://bili2233.cn/BV1ys4y1E7sd", False),  # 过时带协议头
    ("前缀http://b23.tv/BV1234567890", False),     # 过时含前缀
    ("HTTPS://B23.TV/BV1AaBbCcDd", False),  # 过时大小写混合
    ("bili2233.cn/BV1A2B3C4D5E", False),    # 过时无协议头
    ("b23.tv/BV123", False),               # BV号过短
    ("example.com/BV1A441v7e7", False),    # 错误域名
    ("b23.tv/BV1@#$%67890", False)         # 非法字符
]

def test_regex():
    for url, expected in test_cases:
        match = regex.search(url)
        
        # 显示匹配结果
        if match and expected:
            print(f"[✓] 通过: {url} -> 提取 BV: {match.group()}")
        else:
            print(f"[×] 失败: {url} (预期: {expected}, 实际: {not expected})")

def test_short_url_redirects_parse():
    import requests
    for url, expected in test_cases:
        match = regex.search(url)
        if match and expected:
            response = requests.get(match.group(), allow_redirects=False)
            print("[✓] y: 重定向地址: ", response.headers['Location'])
    
    
if __name__ == "__main__":
    try:
        test_regex()
    except re.error as e:
        print(f"正则表达式错误: {e}")
    except Exception as e:
        print(f"运行时错误: {e}")
        
    test_short_url_redirects_parse()