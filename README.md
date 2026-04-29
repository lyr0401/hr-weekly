# 滴滴 HR 资讯 · AI 实时聚合

每 2 小时自动更新，由 Claude AI + 网络搜索驱动。

## 模块

| 模块 | 子分类 |
|------|--------|
| 互联网行业政策法规 | 劳动合同与用工 · 社保/公积金/个税 · 数据安全与员工隐私 |
| 人才市场动向 | 科技岗位动态 · 运营与职能岗位 · 应届生与校招 · 高端人才与猎头 |
| 竞对组织动态 | 组织架构调整 · 裁员与扩招 · 高管人事变动 |
| 薪酬激励参考 | 基础薪资与调薪 · 股权与长期激励 · 福利与弹性补贴 |
| 员工关系与职场舆情 | 劳动仲裁典型案例 · 互联网行业劳动争议 · 职场热点话题预警 |
| HR科技与效能工具 | 招聘与人才测评 · 绩效与员工管理 · AI对HR的影响 |
| 雇主品牌动态 | 大厂雇主品牌动作 · 招聘平台口碑与评分 · 职场文化与价值观趋势 |

## 部署步骤

### 1. 创建仓库
GitHub 创建新仓库，命名为 `hr-weekly`，上传本项目所有文件。

### 2. 添加 API Key
仓库 → Settings → Secrets and variables → Actions → New repository secret
- Name: `ANTHROPIC_API_KEY`
- Value: 你的 Anthropic API Key（https://console.anthropic.com）

### 3. 开启 GitHub Pages
仓库 → Settings → Pages → Source: `Deploy from a branch` → Branch: `main` / `/docs`

### 4. 手动触发第一次生成
仓库 → Actions → 生成滴滴HR资讯 → Run workflow

约 3–5 分钟后访问：`https://你的用户名.github.io/hr-weekly/`

## 修改更新频率

编辑 `.github/workflows/generate.yml` 中 cron 表达式：
- 每1小时：`0 * * * *`
- 每2小时：`0 0,2,4,6,8,10,12,14,16,18,20,22 * * *`
- 每6小时：`0 0,6,12,18 * * *`

## 费用参考

每次生成调用约 20 次 Claude API（7模块×3子项，部分4子项），每次约 ¥1–3，每天12次更新约 ¥12–36。
