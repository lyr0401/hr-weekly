#!/usr/bin/env python3
import os, re, datetime, requests

API_KEY = os.environ["ANTHROPIC_API_KEY"]
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
DATE_STR = NOW.strftime("%Y年%m月%d日 %H:%M")
DATE_CN = NOW.strftime("%Y年%m月%d日")

COMPETITORS = "字节跳动、美团、快手、百度、阿里巴巴、腾讯、货拉拉、嘀嗒出行、曹操出行、满帮集团"

PROMPT_SUFFIX = """
输出格式严格如下，每条之间空一行，输出2-3条：

【标题】
摘要：1-2句核心内容，控制在80字以内，信息密度要高。
滴滴视角：一句话说明对滴滴HR的直接影响或启示。
发布时间：该信息的原始发布日期，格式为 YYYY年MM月DD日。如果是旧闻被转载，注明"原发布于XXXX年XX月，近期被转载"。
新鲜度：【最新】（7天内）、【近期】（7-30天）、【背景参考】（30天以上）三选一，并用一句话说明判断理由。
来源：来源名称 | 完整URL

严格要求：
- 只引用真实存在的内容，绝对不能编造事件、数据或URL
- 必须核查原始发布时间，不要被转载日期误导
- 如果找不到原始发布时间，标注"发布时间：未知"
- 来源优先选择：人社部/国家网信办官网、36Kr、虎嗅、界面新闻、第一财经、澎湃新闻、LinkedIn、脉脉、看准网
- 宁可少输出一条，也不要输出无法核实来源的内容
- 不要输出序号、markdown符号（不要**加粗**）
"""

SECTIONS = [
    {
        "id": "policy",
        "title": "互联网行业政策法规",
        "color": "teal",
        "tag": "Policy",
        "subsections": [
            {
                "id": "policy_labor",
                "title": "劳动合同与用工",
                "prompt": f"你是HR政策专家，请搜索{DATE_CN}前后中国互联网行业劳动合同、用工管理最新政策，重点关注AI时代用工形式变化、算法管理劳动关系、远程办公规范等新议题。" + PROMPT_SUFFIX
            },
            {
                "id": "policy_social",
                "title": "社保 / 公积金 / 个税",
                "prompt": f"你是HR政策专家，请搜索{DATE_CN}前后社保、公积金、个税最新政策动态，包括缴费基数调整、新规落地、各地差异，优先选择官方来源。" + PROMPT_SUFFIX
            },
            {
                "id": "policy_data",
                "title": "数据安全与员工隐私",
                "prompt": f"你是HR合规专家，请搜索{DATE_CN}前后数据安全法、个人信息保护相关监管动态，重点关注AI用于员工管理（算法考核、情绪识别、行为监控）的合规边界。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "talent",
        "title": "人才市场动向",
        "color": "blue",
        "tag": "Talent",
        "subsections": [
            {
                "id": "talent_tech",
                "title": "科技岗位动态（算法 / 研发 / 产品）",
                "prompt": f"你是人才市场分析师，请搜索{DATE_CN}前后中国算法、研发、产品岗位最新供需动态，重点关注AI替代哪些岗位、哪些新岗位因AI崛起、出行&自动驾驶方向人才竞争态势，尽量包含薪资数据。" + PROMPT_SUFFIX
            },
            {
                "id": "talent_ops",
                "title": "运营与职能岗位动态",
                "prompt": f"你是人才市场分析师，请搜索{DATE_CN}前后互联网企业运营、市场、财务、法务、HR等职能岗位招聘趋势，重点关注AI工具对这些岗位的冲击和转型方向。" + PROMPT_SUFFIX
            },
            {
                "id": "talent_campus",
                "title": "应届生与校招趋势",
                "prompt": f"你是校招专家，请搜索{DATE_CN}前后互联网行业校园招聘最新动态，包括各大厂校招进展、offer薪资水平、应届生就业意向变化，重点关注AI时代校招岗位结构变化。" + PROMPT_SUFFIX
            },
            {
                "id": "talent_exec",
                "title": "高端人才与猎头市场",
                "prompt": f"你是猎头行业分析师，请搜索{DATE_CN}前后中国互联网行业高端人才市场动态，重点关注AI时代哪类高管最抢手（首席AI官、算法VP等）、猎头市场热门需求变化、高管薪酬包趋势。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "competitor",
        "title": "竞对组织动态",
        "color": "purple",
        "tag": "Competitor",
        "subsections": [
            {
                "id": "comp_org",
                "title": "组织架构调整",
                "prompt": f"你是企业组织研究员，请搜索{DATE_CN}前后以下公司的组织架构调整：{COMPETITORS}。重点关注因AI战略调整引发的组织变革、业务合并、汇报关系重构，每条注明公司名。" + PROMPT_SUFFIX
            },
            {
                "id": "comp_headcount",
                "title": "裁员与扩招",
                "prompt": f"你是HR市场观察员，请搜索{DATE_CN}前后以下公司的裁员或扩招动态：{COMPETITORS}。重点关注AI驱动的岗位削减或新增，注明规模、涉及部门。" + PROMPT_SUFFIX
            },
            {
                "id": "comp_exec",
                "title": "高管人事变动",
                "prompt": f"你是企业人事动态观察员，请搜索{DATE_CN}前后以下公司VP级及以上高管变动：{COMPETITORS}。包括任命、离职、岗位调整，注明公司和姓名。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "compensation",
        "title": "薪酬激励参考",
        "color": "amber",
        "tag": "Comp & Ben",
        "subsections": [
            {
                "id": "comp_salary",
                "title": "基础薪资与调薪",
                "prompt": f"你是薪酬分析师，请搜索{DATE_CN}前后互联网大厂基础薪资、调薪节奏最新数据，包括调薪比例、时间节点、冻薪情况，尽量包含具体数字和对标公司。" + PROMPT_SUFFIX
            },
            {
                "id": "comp_equity",
                "title": "股权与长期激励",
                "prompt": f"你是薪酬激励专家，请搜索{DATE_CN}前后互联网大厂股权激励（RSU、期权）最新动态，重点关注AI时代股权激励策略变化、新兴岗位授予政策。" + PROMPT_SUFFIX
            },
            {
                "id": "comp_benefits",
                "title": "福利与弹性补贴",
                "prompt": f"你是福利设计专家，请搜索{DATE_CN}前后互联网大厂员工福利创新，重点关注AI时代出现的新型福利（AI工具订阅补贴、技能再培训补贴等）及弹性福利趋势。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "er",
        "title": "员工关系与职场舆情",
        "color": "coral",
        "tag": "ER",
        "subsections": [
            {
                "id": "er_arbitration",
                "title": "劳动仲裁典型案例",
                "prompt": f"你是劳动法专家，请搜索{DATE_CN}前后互联网行业劳动仲裁典型案例，重点关注AI算法考核引发的争议、竞业限制纠纷、绩效末位淘汰争议，注明裁决结果及HR启示。" + PROMPT_SUFFIX
            },
            {
                "id": "er_dispute",
                "title": "互联网行业劳动争议",
                "prompt": f"你是劳动关系观察员，请搜索{DATE_CN}前后互联网企业员工集体投诉、维权事件，重点关注因AI裁员、算法管理引发的新型劳动争议。" + PROMPT_SUFFIX
            },
            {
                "id": "er_trend",
                "title": "职场热点话题预警",
                "prompt": f"你是职场舆情分析师，请搜索{DATE_CN}前后互联网职场热点话题，重点关注AI焦虑、技能淘汰担忧、人机协作摩擦、心理健康等对员工情绪有影响的议题，分析HR需提前应对的点。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "hrtech",
        "title": "HR科技与效能工具",
        "color": "green",
        "tag": "HR Tech",
        "subsections": [
            {
                "id": "hrtech_recruit",
                "title": "招聘与人才测评",
                "prompt": f"你是HR科技分析师，请搜索{DATE_CN}前后AI招聘工具、人才测评平台最新动态，重点关注大模型在简历筛选、面试评估、人才预测中的最新应用，适合大型互联网企业的产品。" + PROMPT_SUFFIX
            },
            {
                "id": "hrtech_perf",
                "title": "绩效与员工管理",
                "prompt": f"你是HR科技分析师，请搜索{DATE_CN}前后AI驱动的绩效管理、员工体验、组织效能工具最新动态，重点关注互联网大厂实际在用的产品和效果数据。" + PROMPT_SUFFIX
            },
            {
                "id": "hrtech_ai",
                "title": "AI 对 HR 职能的重塑",
                "prompt": f"你是AI与未来工作研究员，请搜索{DATE_CN}前后权威报告或案例，关注AI正在重塑HR哪些职能（招聘、培训、绩效、BP等），哪些HR工作被自动化，HR如何转型为AI时代的战略伙伴。" + PROMPT_SUFFIX
            },
        ]
    },
    {
        "id": "employer",
        "title": "雇主品牌动态",
        "color": "pink",
        "tag": "Employer Brand",
        "subsections": [
            {
                "id": "eb_action",
                "title": "大厂雇主品牌动作",
                "prompt": f"你是雇主品牌专家，请搜索{DATE_CN}前后互联网大厂雇主品牌动作，重点关注AI时代各公司如何塑造技术驱动、人才友好的雇主形象，包括校招宣传、员工故事、职场文化对外传播。" + PROMPT_SUFFIX
            },
            {
                "id": "eb_reputation",
                "title": "招聘平台口碑与评分",
                "prompt": f"你是雇主品牌研究员，请搜索{DATE_CN}前后脉脉、看准网、LinkedIn上互联网公司雇主评分变化和员工评价热点，重点关注出行、科技行业，尤其是涉及AI转型期员工体验的讨论。" + PROMPT_SUFFIX
            },
            {
                "id": "eb_culture",
                "title": "职场文化与价值观趋势",
                "prompt": f"你是职场文化观察员，请搜索{DATE_CN}前后互联网行业职场文化最新趋势，重点关注AI时代组织文化变革（人机协作文化、持续学习文化、心理安全感）及代际差异管理新实践。" + PROMPT_SUFFIX
            },
        ]
    },
]

COLOR_MAP = {
    "teal":   {"dot": "#1D9E75", "header_bg": "#F0FAF6", "tag_bg": "#D1F0E4", "tag_fg": "#0A5C40", "sub_accent": "#1D9E75"},
    "blue":   {"dot": "#2E7DD1", "header_bg": "#EEF5FC", "tag_bg": "#CFDFF6", "tag_fg": "#14467A", "sub_accent": "#2E7DD1"},
    "purple": {"dot": "#6B5ED6", "header_bg": "#F2F1FD", "tag_bg": "#DCD9F9", "tag_fg": "#3D3490", "sub_accent": "#6B5ED6"},
    "amber":  {"dot": "#D48A10", "header_bg": "#FDF6E8", "tag_bg": "#FAE4A8", "tag_fg": "#7A4E00", "sub_accent": "#D48A10"},
    "coral":  {"dot": "#C24E28", "header_bg": "#FDF0EB", "tag_bg": "#F8D0C0", "tag_fg": "#8A2E10", "sub_accent": "#C24E28"},
    "green":  {"dot": "#4E8C1A", "header_bg": "#F2F8EA", "tag_bg": "#D4EDBA", "tag_fg": "#2E5A08", "sub_accent": "#4E8C1A"},
    "pink":   {"dot": "#C2406A", "header_bg": "#FDF0F4", "tag_bg": "#F8CCDA", "tag_fg": "#8A1F42", "sub_accent": "#C2406A"},
}

FRESHNESS_COLOR = {
    "最新":   {"bg": "#E1F5EE", "fg": "#0A5C40"},
    "近期":   {"bg": "#FDF6E8", "fg": "#7A4E00"},
    "背景参考": {"bg": "#F0EDE8", "fg": "#6B6560"},
}

def call_claude(prompt):
    resp = requests.post(
        "https://api.gptsapi.net/v1/messages",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 2048,
            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()
    return "".join(b["text"] for b in data["content"] if b["type"] == "text").strip()

def parse_items(text):
    items = []
    current = {}

    def flush():
        if current.get("title"):
            items.append(dict(current))
        current.clear()

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("【") and "】" in line:
            flush()
            current["title"] = line[line.index("【")+1:line.index("】")]
            current.update({"summary":"","didi":"","pub_date":"","freshness":"","freshness_reason":"","source_name":"","source_url":""})
        elif re.match(r'^摘要[：:]', line):
            current["summary"] = re.sub(r'^摘要[：:]', '', line).strip()
        elif re.match(r'^滴滴视角[：:]', line):
            current["didi"] = re.sub(r'^滴滴视角[：:]', '', line).strip()
        elif re.match(r'^发布时间[：:]', line):
            current["pub_date"] = re.sub(r'^发布时间[：:]', '', line).strip()
        elif re.match(r'^新鲜度[：:]', line):
            val = re.sub(r'^新鲜度[：:]', '', line).strip()
            m = re.search(r'【(最新|近期|背景参考)】', val)
            if m:
                current["freshness"] = m.group(1)
                current["freshness_reason"] = val[m.end():].strip().lstrip("，,、：: ")
            else:
                current["freshness_reason"] = val
        elif re.match(r'^来源[：:]', line):
            src = re.sub(r'^来源[：:]', '', line).strip()
            if "|" in src:
                parts = src.split("|", 1)
                current["source_name"] = parts[0].strip()
                current["source_url"] = parts[1].strip()
            else:
                url_match = re.search(r'https?://\S+', src)
                if url_match:
                    current["source_url"] = url_match.group()
                    current["source_name"] = src[:url_match.start()].strip().rstrip("|·· ") or "来源"
                else:
                    current["source_name"] = src

    flush()
    return items

def render_items(items):
    if not items:
        return '<div class="item empty">暂无相关数据</div>'
    html = ""
    for item in items:
        freshness = item.get("freshness", "")
        fc = FRESHNESS_COLOR.get(freshness, {"bg": "#F0EDE8", "fg": "#6B6560"})
        reason = item.get("freshness_reason", "")
        freshness_html = ""
        if freshness:
            title_attr = f' title="{reason}"' if reason else ""
            freshness_html = f'<span class="badge-freshness" style="background:{fc["bg"]};color:{fc["fg"]}"{title_attr}>{freshness}</span>'

        pub_date = item.get("pub_date", "")
        date_html = f'<span class="pub-date">📅 {pub_date}</span>' if pub_date else ""
        summary_html = f'<div class="item-summary">{item["summary"]}</div>' if item.get("summary") else ""
        didi_html = f'<div class="item-didi"><span class="didi-label">滴滴视角</span>{item["didi"]}</div>' if item.get("didi") else ""

        source_html = ""
        if item.get("source_url") and item["source_url"].startswith("http"):
            name = item.get("source_name") or "查看来源"
            source_html = f'<a class="source-link" href="{item["source_url"]}" target="_blank" rel="noopener">↗ {name}</a>'
        elif item.get("source_name"):
            source_html = f'<span class="source-text">来源：{item["source_name"]}</span>'

        html += f"""<div class="item">
  <div class="item-header">
    <div class="item-title">{item.get("title","")}</div>
    <div class="item-meta">{freshness_html}{date_html}</div>
  </div>
  {summary_html}{didi_html}
  <div class="item-footer">{source_html}</div>
</div>"""
    return html

def render_section(section):
    c = COLOR_MAP[section["color"]]
    subs_html = ""
    for sub in section["subsections"]:
        items_html = sub.get("items_html", '<div class="item empty">加载失败，请等待下次更新</div>')
        subs_html += f"""<div class="subsection">
  <div class="subsection-header">
    <span class="sub-accent" style="background:{c['sub_accent']}"></span>
    <span class="subsection-title">{sub['title']}</span>
  </div>
  <div class="subsection-body">{items_html}</div>
</div>"""
    return f"""<div class="section-card" id="{section['id']}">
  <div class="section-header" style="background:{c['header_bg']}">
    <span class="dot" style="background:{c['dot']}"></span>
    <span class="section-title">{section['title']}</span>
    <span class="section-tag" style="background:{c['tag_bg']};color:{c['tag_fg']}">{section['tag']}</span>
  </div>
  <div class="section-body">{subs_html}</div>
</div>"""

def build_html(sections_html):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="28800">
<title>滴滴 HR 资讯 · 实时更新</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=DM+Mono&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans SC',sans-serif;background:#F4F2EE;color:#1A1816;min-height:100vh;font-size:14px;line-height:1.6}}
.masthead{{background:#111;color:#fff;border-bottom:3px solid #FF5F00}}
.masthead-inner{{max-width:860px;margin:0 auto;padding:1.25rem 1.5rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand-logo{{width:36px;height:36px;background:#FF5F00;border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'DM Mono',monospace;font-size:12px;font-weight:600;color:#fff;flex-shrink:0}}
.brand-name{{font-size:16px;font-weight:600;letter-spacing:-.02em}}
.brand-sub{{font-size:11px;color:rgba(255,255,255,.4);margin-top:2px}}
.meta{{text-align:right;flex-shrink:0}}
.meta-freq{{font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,.35);margin-bottom:3px}}
.meta-time{{font-family:'DM Mono',monospace;font-size:12px;color:rgba(255,255,255,.6)}}
.page{{max-width:860px;margin:0 auto;padding:1.25rem 1.5rem 3rem}}
.nav{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1.5rem;padding-bottom:1.25rem;border-bottom:.5px solid #DDD9D3}}
.nav-item{{font-size:11px;padding:5px 12px;border-radius:20px;border:.5px solid #DDD9D3;color:#6B6560;text-decoration:none;background:#fff;transition:all .15s;white-space:nowrap}}
.nav-item:hover{{border-color:#1A1816;color:#1A1816}}
.section-card{{background:#fff;border:.5px solid #DDD9D3;border-radius:12px;overflow:hidden;margin-bottom:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.section-header{{display:flex;align-items:center;gap:10px;padding:14px 18px;border-bottom:.5px solid #DDD9D3}}
.dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.section-title{{font-size:13px;font-weight:600;flex:1;letter-spacing:-.01em}}
.section-tag{{font-size:10px;padding:2px 9px;border-radius:10px;white-space:nowrap;font-family:'DM Mono',monospace}}
.subsection{{border-bottom:.5px solid #EEEAE4}}
.subsection:last-child{{border-bottom:none}}
.subsection-header{{display:flex;align-items:center;padding:10px 18px;background:#FAFAF8}}
.sub-accent{{width:3px;height:14px;border-radius:2px;flex-shrink:0;margin-right:10px}}
.subsection-title{{font-size:12px;font-weight:500;color:#4A4540}}
.item{{padding:14px 18px;border-bottom:.5px solid #F2EEE8}}
.item:last-child{{border-bottom:none}}
.item.empty{{color:#A09A93;font-size:12px;padding:14px 18px}}
.item-header{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:7px}}
.item-title{{font-size:13px;font-weight:600;color:#1A1816;line-height:1.5;flex:1}}
.item-meta{{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0;padding-top:1px}}
.badge-freshness{{font-size:10px;padding:2px 7px;border-radius:8px;white-space:nowrap;font-family:'DM Mono',monospace;cursor:default;letter-spacing:.01em}}
.pub-date{{font-family:'DM Mono',monospace;font-size:10px;color:#A09A93;white-space:nowrap}}
.item-summary{{font-size:12.5px;color:#3A3530;line-height:1.8;margin-bottom:8px}}
.item-didi{{font-size:12px;color:#5A5550;background:#FDF5F0;border-left:2px solid #FF5F00;border-radius:0 6px 6px 0;padding:7px 10px;margin-bottom:9px;line-height:1.65}}
.didi-label{{display:inline-block;font-size:10px;font-weight:600;color:#FF5F00;margin-right:6px;font-family:'DM Mono',monospace;letter-spacing:.02em}}
.item-footer{{display:flex;align-items:center}}
.source-link{{font-size:11px;color:#2E7DD1;text-decoration:none;padding:3px 9px;border:.5px solid #CFDFF6;border-radius:6px;background:#EEF5FC;transition:all .15s}}
.source-link:hover{{background:#CFDFF6;border-color:#2E7DD1}}
.source-text{{font-size:11px;color:#A09A93}}
.footer{{text-align:center;font-size:11px;color:#A09A93;margin-top:1.5rem;font-family:'DM Mono',monospace;line-height:2.2}}
.footer-badges{{display:inline-flex;gap:6px;margin:0 4px;vertical-align:middle}}
.fb{{padding:1px 7px;border-radius:4px;font-size:10px}}
@media(max-width:600px){{
  .masthead-inner{{flex-direction:column;align-items:flex-start;gap:.75rem}}
  .meta{{text-align:left}}
  .item-header{{flex-direction:column;gap:5px}}
  .item-meta{{flex-direction:row;align-items:center}}
  .page{{padding:1rem 1rem 2rem}}
}}
</style>
</head>
<body>
<div class="masthead">
  <div class="masthead-inner">
    <div class="brand">
      <div class="brand-logo">HR</div>
      <div>
        <div class="brand-name">滴滴 HR 资讯</div>
        <div class="brand-sub">内部员工 · AI 实时聚合 · 仅供内部参考</div>
      </div>
    </div>
    <div class="meta">
      <div class="meta-freq">每日更新 08:00 / 14:00 / 21:00</div>
      <div class="meta-time">更新于 {DATE_STR} CST</div>
    </div>
  </div>
</div>
<div class="page">
  <nav class="nav">
    <a class="nav-item" href="#policy">📋 政策法规</a>
    <a class="nav-item" href="#talent">👥 人才市场</a>
    <a class="nav-item" href="#competitor">🔍 竞对动态</a>
    <a class="nav-item" href="#compensation">💰 薪酬激励</a>
    <a class="nav-item" href="#er">⚖️ 员工关系</a>
    <a class="nav-item" href="#hrtech">🤖 HR科技</a>
    <a class="nav-item" href="#employer">🏆 雇主品牌</a>
  </nav>
  {sections_html}
  <div class="footer">
    仅供内部参考 · 由 Claude AI + 网络搜索驱动 · 请点击来源链接核实原文<br>
    新鲜度：
    <span class="fb" style="background:#E1F5EE;color:#0A5C40">最新</span> 7天内 &nbsp;
    <span class="fb" style="background:#FDF6E8;color:#7A4E00">近期</span> 7–30天 &nbsp;
    <span class="fb" style="background:#F0EDE8;color:#6B6560">背景参考</span> 30天以上（鼠标悬停查看判断理由）<br>
    竞对范围：字节跳动 · 美团 · 快手 · 百度 · 阿里巴巴 · 腾讯 · 货拉拉 · 嘀嗒 · 曹操出行 · 满帮
  </div>
</div>
</body>
</html>"""

def main():
    print(f"开始生成，时间：{DATE_STR}")
    total = sum(len(s["subsections"]) for s in SECTIONS)
    done = 0
    for section in SECTIONS:
        print(f"\n[{section['title']}]")
        for sub in section["subsections"]:
            print(f"  ▶ {sub['title']} ...", end=" ", flush=True)
            try:
                text = call_claude(sub["prompt"])
                items = parse_items(text)
                if not items:
                    items = [{"title":"暂无数据","summary":text[:150] if text else "","didi":"","pub_date":"","freshness":"","freshness_reason":"","source_name":"","source_url":""}]
                sub["items_html"] = render_items(items)
                print(f"✅ ({len(items)}条)")
            except Exception as e:
                print(f"❌ {e}")
                sub["items_html"] = render_items([])
            done += 1
            print(f"     进度 {done}/{total}")

    sections_html = "".join(render_section(s) for s in SECTIONS)
    html = build_html(sections_html)
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n✅ 全部完成！已生成 docs/index.html")

if __name__ == "__main__":
    main()
