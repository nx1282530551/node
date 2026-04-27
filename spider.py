import requests
import random
import time
import re
import datetime

# ==============================================
# 爬虫 1：每 4 小时更新
# ==============================================
def crawl1():
    try:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7); rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.2420.81 Safari/537.36     Edg/123.0.2420.81',
            'Mozilla/5.0 (Windows NT 10.0; Win32); rv:115.0) Gecko/20100101 Firefox/115.0'
        ]
        url = "https://github.com/WLget/V2Ray_configs_64"
        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        page_source = response.text
        keyword_start = 'v2ray免费节点订阅'
        keyword_end = 'Clash免费节点订阅'
        start_index = page_source.find(keyword_start)
        if start_index == -1:
            return "1：未找到内容"
        end_index = page_source.find(keyword_end, start_index)
        if end_index == -1:
            return "1：未找到结束标识"
        text = page_source[start_index:end_index + len(keyword_end)]
        start = text.find('http')
        end = text.find('\\', start)
        if start != -1 and end != -1:
            return text[start:end]
        return "1：未提取到有效链接"
    except Exception as e:
        return f"1异常：{str(e)}"

# ==============================================
# 爬虫 2：每 1 小时更新
# ==============================================
def crawl2():
    try:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/517.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/427.16',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/527.46',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/327.46'
        ]
        url = 'https://github.com/abshare3/abshare3.github.io'
        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        page_source = response.text
        keyword_start = '免费v2rayN订阅链接'
        keyword_end = '费iOS小火箭订阅链接'
        start_index = page_source.find(keyword_start)
        if start_index == -1:
            return "未找到内容"
        end_index = page_source.find(keyword_end, start_index)
        if end_index == -1:
            return "未找到结束标识"
        text = page_source[start_index:end_index + len(keyword_end)]
        start = text.find('https')
        end = text.find('\\', start)
        if start != -1 and end != -1:
            return text[start:end]
        return "未提取到有效链接"
    except Exception as e:
        return f"{str(e)}"

# ==============================================
# 生成带复制按钮的链接
# ==============================================
def make_copy_btn(link):
    if not link or "未找到" in link or "异常" in link:
        return f"<span>{link}</span>"
    return f'''
<span>{link}</span>
<button onclick="navigator.clipboard.writeText('{link}').then(()=>alert('复制成功！')).catch(()=>alert('复制失败，请手动复制'))"
style="margin-left:8px; padding:2px 8px; background:#007bff; color:white; border:none; border-radius:4px; cursor:pointer;">
一键复制
</button>
'''.strip()

# ==============================================
# 写入 README.md
# ==============================================
if __name__ == "__main__":
    data1 = crawl1()
    data2 = crawl2()

    # 生成带按钮的内容
    data1_with_btn = make_copy_btn(data1)
    data2_with_btn = make_copy_btn(data2)

    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    update_time = now.strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# 自动更新订阅

## 长node更新
{data1_with_btn}

## 短node更新
{data2_with_btn}

---
⏱ 全量更新时间：{update_time}（东八区）
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content.strip())
