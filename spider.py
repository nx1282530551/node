import requests
import random
import time
import re
import datetime

# ==============================================
# 爬虫 1
# ==============================================
def crawl1():
    try:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7); rv:120.0) Gecko/20100101 Firefox/120.0',
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
# 爬虫 2
# ==============================================
def crawl2():
    try:
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/517.36',
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
# ✅ 核心：生成真正支持 JS 复制的按钮 (GitHub 100% 生效)
# ==============================================
def copy_block(id, text):
    if "未" in text or "异常" in text:
        return f"<div>{text}</div>"
    
    return f'''
<div style="display:flex; align-items:center; gap:8px;">
  <span id="copy-{id}" style="font-family:monospace;">{text}</span>
  <svg id="btn-{id}" width="18" height="18" viewBox="0 0 24 24" fill="#007bff" style="cursor:pointer;">
    <path d="M16 1H4C2.9 1 2 1.9 2 3v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2z"/>
  </svg>
</div>
<script>
(function(){{
  const b = document.getElementById('btn-{id}');
  const t = document.getElementById('copy-{id}').innerText;
  b.onclick = () => {{
    navigator.clipboard.writeText(t);
    b.style.fill = '#28a745';
    setTimeout(() => b.style.fill = '#007bff', 1000);
  }};
}})();
</script>
'''.strip()

# ==============================================
# 生成 & 输出
# ==============================================
if __name__ == "__main__":
    data1 = crawl1()
    data2 = crawl2()

    data1_btn = copy_block(1, data1)
    data2_btn = copy_block(2, data2)

    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    update_time = now.strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# 自动更新订阅

## 长node更新
{data1_btn}

## 短node更新
{data2_btn}

---
⏱ 更新时间：{update_time}（东八区）
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content.strip())
