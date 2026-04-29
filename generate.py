#!/usr/bin/env python3
import os, datetime, requests

API_KEY = os.environ["ANTHROPIC_API_KEY"]
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
DATE_STR = NOW.strftime("%Y年%m月%d日 %H:%M")
DATE_CN = NOW.strftime("%Y年%m月%d日")

COMPETITORS = "字节跳动、美团、快手、百度、阿里巴巴、腾讯、货拉拉、嘀嗒出行、曹操出行、满帮集团"

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
                "prompt": f"你是HR政策专家。请搜索{DATE_CN}前后，中国互联网行业劳动合同、用工管理相关的最新政策法规动态，包括劳动法修订、用工形式规范、试用期管理、裁员补偿等。输出2-3条，每条格式：\n【标题】\n一到两句说明，突出对互联网企业HR的影响。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "policy_social",
                "title": "社保 / 公积金 / 个税",
                "prompt": f"你是HR政策专家。请搜索{DATE_CN}前后，中国社保、公积金、个人所得税最新政策动态，包括缴费基数调整、新规落地、各地差异等。输出2-3条，每条格式：\n【标题】\n一到两句说明，突出对企业HR操作的影响。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "policy_data",
                "title": "数据安全与员工隐私",
                "prompt": f"你是HR合规专家。请搜索{DATE_CN}前后，中国数据安全法、个人信息保护法相关的最新监管动态，重点关注涉及员工数据、招聘数据、HR系统合规要求的部分。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是人才市场分析师。请搜索{DATE_CN}前后，中国算法工程师、软件研发、产品经理等科技岗位的最新供需动态，包括热门方向、薪资变化、供需紧张程度。输出2-3条，每条格式：\n【标题】\n一到两句说明，尽量包含具体数据。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "talent_ops",
                "title": "运营与职能岗位动态",
                "prompt": f"你是人才市场分析师。请搜索{DATE_CN}前后，中国互联网企业运营、市场、财务、法务、HR等职能岗位的最新招聘趋势，包括需求变化、薪资水平、热门技能要求。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "talent_campus",
                "title": "应届生与校招趋势",
                "prompt": f"你是校招专家。请搜索{DATE_CN}前后，中国互联网行业校园招聘最新动态，包括各大厂校招进展、应届生就业意向变化、薪资offer水平、高校合作动态。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "talent_exec",
                "title": "高端人才与猎头市场",
                "prompt": f"你是猎头行业分析师。请搜索{DATE_CN}前后，中国互联网行业高端人才市场动态，包括总监级及以上人才流动、猎头市场热门需求、高管薪酬包变化趋势。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是企业组织研究员。请搜索{DATE_CN}前后，以下互联网公司的组织架构调整动态：{COMPETITORS}。包括业务合并、部门拆分、汇报关系变化等。输出2-3条，每条格式：\n【公司名·事件】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "comp_headcount",
                "title": "裁员与扩招",
                "prompt": f"你是HR市场观察员。请搜索{DATE_CN}前后，以下互联网公司的裁员或大规模招聘动态：{COMPETITORS}。包括规模、涉及部门、原因分析。输出2-3条，每条格式：\n【公司名·事件】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "comp_exec",
                "title": "高管人事变动",
                "prompt": f"你是企业人事动态观察员。请搜索{DATE_CN}前后，以下互联网公司高管（VP级及以上）的人事变动：{COMPETITORS}。包括任命、离职、岗位调整。输出2-3条，每条格式：\n【公司名·姓名·变动】\n一到两句背景说明。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是薪酬分析师。请搜索{DATE_CN}前后，中国互联网大厂（{COMPETITORS}）基础薪资、调薪节奏的最新数据或报告，包括调薪比例、调薪时间、冻薪情况。输出2-3条，每条格式：\n【标题】\n一到两句说明，尽量包含具体数字。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "comp_equity",
                "title": "股权与长期激励",
                "prompt": f"你是薪酬激励专家。请搜索{DATE_CN}前后，中国互联网大厂股权激励（RSU、期权）最新动态，包括授予范围、兑现条件、市值变化对激励效果的影响。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "comp_benefits",
                "title": "福利与弹性补贴",
                "prompt": f"你是福利设计专家。请搜索{DATE_CN}前后，中国互联网大厂员工福利创新动态，包括弹性福利、健康险、居家办公补贴、生育福利等新举措。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是劳动法专家。请搜索{DATE_CN}前后，中国互联网行业劳动仲裁或法院判决的典型案例，重点关注对企业HR实操有参考价值的案例，如竞业限制、N+1补偿、绩效末位淘汰等。输出2-3条，每条格式：\n【案例标题】\n一到两句说明裁决结果及HR启示。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "er_dispute",
                "title": "互联网行业劳动争议",
                "prompt": f"你是劳动关系观察员。请搜索{DATE_CN}前后，中国互联网企业员工集体投诉、劳动争议、维权事件的最新动态，包括事件经过和企业应对方式。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "er_trend",
                "title": "职场热点话题预警",
                "prompt": f"你是职场舆情分析师。请搜索{DATE_CN}前后，中国互联网职场热点话题，包括加班文化、绩效管理、职场歧视、心理健康等可能引发员工情绪波动的社会议题。输出2-3条，每条格式：\n【话题标题】\n一到两句说明HR需关注的点。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是HR科技分析师。请搜索{DATE_CN}前后，招聘平台、AI面试、人才测评工具的最新产品动态或行业资讯，重点关注对大型互联网企业有价值的工具。输出2-3条，每条格式：\n【产品/公司名】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "hrtech_perf",
                "title": "绩效与员工管理",
                "prompt": f"你是HR科技分析师。请搜索{DATE_CN}前后，绩效管理系统、OKR工具、员工体验平台的最新产品动态，重点关注互联网大厂在用或关注的工具。输出2-3条，每条格式：\n【产品/公司名】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "hrtech_ai",
                "title": "AI 对 HR 的影响",
                "prompt": f"你是AI与未来工作研究员。请搜索{DATE_CN}前后，AI技术对HR工作影响的最新报告、案例或讨论，包括AI替代HR工作、HR用AI提效、AI带来的用工变化等。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
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
                "prompt": f"你是雇主品牌专家。请搜索{DATE_CN}前后，中国互联网大厂（{COMPETITORS}）的雇主品牌营销动作，包括招聘宣传、校招品牌活动、员工故事内容、职场文化对外传播等。输出2-3条，每条格式：\n【公司名·动作】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "eb_reputation",
                "title": "招聘平台口碑与评分",
                "prompt": f"你是雇主品牌研究员。请搜索{DATE_CN}前后，脉脉、看准网（Kanzhun）、LinkedIn等平台上互联网公司雇主评分变化、员工匿名评价热点，重点关注出行、科技行业相关内容。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
            {
                "id": "eb_culture",
                "title": "职场文化与价值观趋势",
                "prompt": f"你是职场文化观察员。请搜索{DATE_CN}前后，中国互联网行业职场文化趋势，包括工作方式变革、多元包容、员工体验、代际差异管理等话题的最新讨论或实践案例。输出2-3条，每条格式：\n【标题】\n一到两句说明。\n直接输出，不要序号和markdown。"
            },
        ]
    },
]

COLOR_MAP = {
    "teal":   {"dot": "#1D9E75", "header_bg": "#F0FAF6", "tag_bg": "#E1F5EE", "tag_fg": "#0F6E56", "sub_border": "#C5EAD9"},
    "blue":   {"dot": "#378ADD", "header_bg": "#F0F6FD", "tag_bg": "#E6F1FB", "tag_fg": "#185FA5", "sub_border": "#C0D9F5"},
    "purple": {"dot": "#7F77DD", "header_bg": "#F4F3FE", "tag_bg": "#EEEDFE", "tag_fg": "#534AB7", "sub_border": "#D0CDFA"},
    "amber":  {"dot": "#EF9F27", "header_bg": "#FDF8EE", "tag_bg": "#FAEEDA", "tag_fg": "#854F0B", "sub_border": "#F5DDA0"},
    "coral":  {"dot": "#D85A30", "header_bg": "#FDF3EF", "tag_bg": "#FAECE7", "tag_fg": "#993C1D", "sub_border": "#F5C9B5"},
    "green":  {"dot": "#639922", "header_bg": "#F4F9EC", "tag_bg": "#EAF3DE", "tag_fg": "#3B6D11", "sub_border": "#C8DFA0"},
    "pink":   {"dot": "#D4537E", "header_bg": "#FDF2F6", "tag_bg": "#FBEAF0", "tag_fg": "#993556", "sub_border": "#F4C0D5"},
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
            "max_tokens": 1024,
            "tools": [{"type": "web_search_20250305", "name": "web_search"}],
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return "".join(b["text"] for b in data["content"] if b["type"] == "text").strip()

def parse_items(text):
    items = []
    current_title = None
    current_desc = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            if current_title:
                items.append({"title": current_title, "desc": " ".join(current_desc)})
                current_title = None
                current_desc = []
            continue
        if line.startswith("【") and "】" in line:
            if current_title:
                items.append({"title": current_title, "desc": " ".join(current_desc)})
                current_desc = []
            current_title = line[line.index("【")+1:line.index("】")]
            rest = line[line.index("】")+1:].strip()
            if rest:
                current_desc = [rest]
        else:
            if current_title:
                current_desc.append(line)
    if current_title:
        items.append({"title": current_title, "desc": " ".join(current_desc)})
    return items

def render_items(items):
    if not items:
        return '<div class="item"><div class="item-desc" style="color:#A09A93">暂无相关数据</div></div>'
    html = ""
    for item in items:
        html += f'<div class="item"><div class="item-title">{item["title"]}</div><div class="item-desc">{item["desc"]}</div></div>'
    return html

def render_section(section):
    c = COLOR_MAP[section["color"]]
    subsections_html = ""
    for sub in section["subsections"]:
        items_html = sub.get("items_html", '<div class="item"><div class="item-desc" style="color:#A09A93">加载失败</div></div>')
        subsections_html += f"""
        <div class="subsection">
          <div class="subsection-header" style="border-left:3px solid {c['dot']}">
            <span class="subsection-title">{sub['title']}</span>
          </div>
          <div class="subsection-body">{items_html}</div>
        </div>"""
    return f"""
  <div class="section-card">
    <div class="section-header" style="background:{c['header_bg']}">
      <span class="dot" style="background:{c['dot']}"></span>
      <span class="section-title">{section['title']}</span>
      <span class="section-tag" style="background:{c['tag_bg']};color:{c['tag_fg']}">{section['tag']}</span>
    </div>
    <div class="section-body">{subsections_html}</div>
  </div>"""

def build_html(sections_html):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="7200">
<title>滴滴 HR 资讯 · 实时更新</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500&family=DM+Mono&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans SC',sans-serif;background:#F7F5F0;color:#1A1816;min-height:100vh}}
.masthead{{background:#1A1816;color:#fff;padding:1.5rem 1.25rem 1.25rem;border-bottom:3px solid #FF5F00}}
.masthead-inner{{max-width:800px;margin:0 auto;display:flex;align-items:flex-end;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:10px}}
.brand-logo{{width:32px;height:32px;background:#FF5F00;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;color:#fff;font-family:'DM Mono',monospace}}
.brand-name{{font-size:17px;font-weight:500}}
.brand-sub{{font-size:12px;color:rgba(255,255,255,.45);margin-top:2px}}
.meta{{text-align:right}}
.meta-freq{{font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,.4);margin-bottom:3px}}
.meta-time{{font-family:'DM Mono',monospace;font-size:12px;color:rgba(255,255,255,.65)}}
.page{{max-width:800px;margin:0 auto;padding:1.5rem 1.25rem 3rem}}
.nav{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1.5rem;padding-bottom:1.25rem;border-bottom:.5px solid #E2DDD6}}
.nav-item{{font-size:11px;padding:4px 10px;border-radius:20px;border:.5px solid #E2DDD6;color:#6B6560;cursor:pointer;text-decoration:none;background:#fff;transition:all .15s}}
.nav-item:hover{{border-color:#1A1816;color:#1A1816}}
.section-card{{background:#fff;border:.5px solid #E2DDD6;border-radius:12px;overflow:hidden;margin-bottom:1.25rem}}
.section-header{{display:flex;align-items:center;gap:10px;padding:13px 16px;border-bottom:.5px solid #E2DDD6}}
.dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.section-title{{font-size:13px;font-weight:500;flex:1}}
.section-tag{{font-size:11px;padding:2px 9px;border-radius:10px;white-space:nowrap}}
.subsection{{border-bottom:.5px solid #F0EDE8}}
.subsection:last-child{{border-bottom:none}}
.subsection-header{{padding:10px 16px;background:#FAFAF8}}
.subsection-title{{font-size:12px;font-weight:500;color:#4A4742;padding-left:8px}}
.subsection-body{{padding:2px 0}}
.item{{padding:10px 16px;border-bottom:.5px solid #F5F2EE}}
.item:last-child{{border-bottom:none}}
.item-title{{font-size:13px;font-weight:500;color:#1A1816;margin-bottom:3px}}
.item-desc{{font-size:12px;color:#6B6560;line-height:1.75}}
.footer{{text-align:center;font-size:11px;color:#A09A93;margin-top:1.5rem;font-family:'DM Mono',monospace;line-height:1.8}}
@media(max-width:600px){{
  .masthead-inner{{flex-direction:column;align-items:flex-start;gap:.75rem}}
  .meta{{text-align:left}}
  .nav{{gap:5px}}
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
        <div class="brand-sub">内部员工 · AI 实时聚合</div>
      </div>
    </div>
    <div class="meta">
      <div class="meta-freq">每2小时自动更新</div>
      <div class="meta-time">更新于 {DATE_STR} CST</div>
    </div>
  </div>
</div>
<div class="page">
  <nav class="nav">
    <a class="nav-item" href="#policy">政策法规</a>
    <a class="nav-item" href="#talent">人才市场</a>
    <a class="nav-item" href="#competitor">竞对动态</a>
    <a class="nav-item" href="#compensation">薪酬激励</a>
    <a class="nav-item" href="#er">员工关系</a>
    <a class="nav-item" href="#hrtech">HR科技</a>
    <a class="nav-item" href="#employer">雇主品牌</a>
  </nav>
  {sections_html}
  <div class="footer">
    仅供内部参考 · 由 Claude AI + 网络搜索驱动 · 建议结合原始来源核实<br>
    竞对范围：字节跳动、美团、快手、百度、阿里巴巴、腾讯、货拉拉、嘀嗒、曹操出行、满帮
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
            print(f"  生成：{sub['title']} ...", end=" ", flush=True)
            try:
                text = call_claude(sub["prompt"])
                items = parse_items(text)
                if not items:
                    items = [{"title": "暂无数据", "desc": text[:200] if text else ""}]
                sub["items_html"] = render_items(items)
                print("✅")
            except Exception as e:
                print(f"❌ {e}")
                sub["items_html"] = render_items([])
            done += 1
            print(f"  进度：{done}/{total}")

    sections_html = ""
    for section in SECTIONS:
        section_html = render_section(section)
        section_html = section_html.replace('<div class="section-card">', f'<div class="section-card" id="{section["id"]}">', 1)
        sections_html += section_html

    html = build_html(sections_html)
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n✅ 完成！已生成 docs/index.html")

if __name__ == "__main__":
    main()
