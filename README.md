# book-commerce-video

把一本书逐步做成可审核、可继续编辑的竖屏推荐视频。

这是一个面向 Codex 的中文 Skill，整理自实际图书视频制作流程：核对版本与读者反馈、确定角度、审核口播、设计分镜、准备素材、直接编辑 ChatCut 时间线，最后检查字幕、动效和平台安全区。

它提供流程与验收标准。完整制作还需要已授权的 ChatCut 插件和图片、配音等服务；安装本仓库不会自动开通这些服务。

## 快速开始

需要 Git；可选安装器和结构检查需要 Python 3.9 或更新版本。使用 Skill 时需要支持本地 Skill 的 Codex 环境。

```bash
git clone https://github.com/anan-beep/book-commerce-video.git
cd book-commerce-video
python3 scripts/install.py
```

安装器默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills/book-commerce-video`，已有同名目录时停止，避免覆盖个人版本。可用 `--dest /path/to/skills` 指定 Skill 父目录。重新打开 Codex 会话或刷新 Skill 列表后调用：

```text
使用 $book-commerce-video，把《纳瓦尔宝典》做成一条约 90 秒的图书推荐视频。
平台：视频号。观众：想重新思考工作与时间安排的成年人。
请先核对版本，给出候选角度和完整口播，等我确认后再制作素材。
```

其他起点见 [使用示例](examples/prompts.md)。只安装本仓库即可获得研究、写稿、分镜和验收指导；实际检索、生成媒体和编辑时间线取决于所在环境的工具与授权。

## 工作流程

| 阶段 | 可审核交付 | 进入下一阶段的条件 |
| --- | --- | --- |
| 研究 | 版本信息、来源、读者问题、候选角度 | 版本明确，角度确认 |
| 口播 | 标题、封面文案、正文、作品简介 | 用户确认口播 |
| 视觉 | 分镜、素材清单、代表性样图 | 用户确认风格与样图 |
| 制作 | 配音、书封轮播、正文、双语字幕、ChatCut 时间线 | 先审核样片，再处理全片 |
| 验收 | 连续播放、音画同步、素材在线、平台安全区 | 用户确认成片或明确要求导出 |

制作基线为 9:16、1080×1920、30 fps，中文主字幕搭配英文辅字幕。时长、语言、开场与风格可按本期目标调整。最终配音决定画面和字幕时间；修改音频后重新对齐。

## 使用依赖

| 能力 | 需要什么 | 不可用时 |
| --- | --- | --- |
| 书籍与读者研究 | 用户授权的浏览器或书籍资料 | 标注缺口，请用户提供材料 |
| 研究增强（可选） | `weread-skills` | 使用公开资料或用户材料 |
| 写作增强（可选） | `short-video-spoken-script` | 使用仓库内写作指导 |
| 图片、配音、音乐 | 可用的生成工具或用户自备素材 | 交付清单与提示词 |
| 时间线与导出 | [ChatCut](https://chatcut.io/) 插件、账号授权及其当前工具说明 | 交付制作方案，明确尚未制作时间线 |
| 结构检查（开发用） | Python + `requirements-dev.txt` | 不影响阅读与使用 Skill |

本项目免费开源。使用前需准备上表所列工具、账号授权或自备素材。通过 Hosted ChatCut MCP 直接编辑时间线，不调用编辑器里的 AI Agent。

第三方 Skill、ChatCut 插件、模型、账号和商业素材不包含在本仓库中，也不由本仓库的 MIT 许可证授权。

## 仓库内容

```text
SKILL.md                       Skill 入口
agents/openai.yaml             Codex 展示信息与 ChatCut 依赖声明
references/                    研究、视觉、制作、验收细则
examples/prompts.md             不同起点的使用示例
evals/evals.json                人工行为评估用例
scripts/install.py             不覆盖已有目录的本地安装器
scripts/validate.py            分发结构、链接、元数据检查
.github/workflows/validate.yml  GitHub Actions 结构检查
```

## 验证与贡献

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

结构检查验证文件、元数据、相对链接与评估用例格式，不能证明已经成功生成或导出视频。`evals/evals.json` 是人工评估任务，尚未运行完整行为评估；修改流程后应按实际环境复测。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 素材与事实

区分书中事实、公开点评和创作推断；引用应能追溯到来源。示例书名只用于演示调用方法。本仓库不分发书籍正文、书封、读者评论原文、声音克隆数据或成片；使用者自行确认所用图片、音乐、字体与声音的使用权限。

公开资料不足时说明缺口，不编造评论、原书观点、客户案例或收入。技术验收不代表流量、销量或平台推荐结果。

## 许可证

[MIT](LICENSE)。允许使用、修改和分发本仓库的原创流程文档及代码；保留许可证和版权声明。
