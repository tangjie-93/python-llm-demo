# 🎮 打怪通关图谱 · AI Agent 游戏化学习地图

> 📺 **推荐**：用浏览器打开 [boss-battle-view.html](./boss-battle-view.html) 获得最佳可视化体验
>
> **玩家职业**：资深前端工程师（Lv.80 TypeScript/React/Vue 战士）
> **终极任务**：转职成为 全栈 AI Agent 工程师
> **预计游玩时间**：22 周 | **总经验值**：110 EXP

---

## 🗺️ 世界地图

```
🌟 AI Agent 大陆 · 世界地图
══════════════════════════════

新手村 ──→ 🌿 翠蛇平原 ──→ 🧠 思维神殿
(起点)     Lv.1-1~4 (4周)    Lv.2-1~3 (3周)
               │                    │
               ▼                    ▼
         📚 知识深渊 ──→ 🤖 机械王都
         Lv.3-1~4 (4周)    Lv.4-1~5 (5周)
               │                    │
               ▼                    ▼
         📡 协议之塔 ──→ 🏰 云端城堡
         Lv.5-1~3 (3周)    Lv.6-1~3 (3周)

🏕️ 补给站: 第4周 → 第11周 → 第19周
🔀 支线: Ollama本地部署 | 前端界面 | DB对比
🔮 隐藏: 模型微调 | Web Agent | Agent Swarm
```

---

## 🏰 六大区域详解

---

## 🌿 阶段一：翠蛇平原 — Python 后端基础

> **区域主题**：从 TypeScript 大陆穿越到 Python 平原，掌握蛇语魔法
> **区域 BOSS**：`🐉 异步魔龙 asyncio` — 拥有强大的并发吐息，需用协程护盾抵挡
> **区域时间**：4 周 | **区域总 EXP**：20

```
🌿 翠蛇平原 · Lv.1-1 → Lv.1-2 → Lv.1-3 → Lv.1-4 → 🏕️ 补给站
   🐍 蛇语觉醒  →  📦 包管理  →  🚀 疾风API →  🗄️ 数据掌控

   BOSS: 🐍 缩进巨蟒   🌀 依赖地狱犬  ⚡ 路由九头蛇  🐉 异步魔龙(区域BOSS)
```

### 🐍 Level 1-1：蛇语觉醒 · Python 基础语法

| 属性 | 内容 |
|------|------|
| **BOSS** | `🐍 缩进巨蟒 IndentationError` — 用严格的缩进纪律约束冒险者 |
| **小怪清单** | `变量哥布林` `函数史莱姆` `列表骷髅兵` `字典石像鬼` `类幽灵` `异常蝙蝠` |
| **掉落装备** | ⚔️ Python 语法之剑 · 🛡️ 类型注解护盾 · 💍 推导式戒指 |
| **EXP** | ⭐⭐ (2/5) — 基础但内容密度大 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 翻译一段 TS 代码为 Python ✅ 实现 @retry 装饰器 ✅ CLI 工具可运行 |

### 📦 Level 1-2：包管理器大师 · 工程化入门

| 属性 | 内容 |
|------|------|
| **BOSS** | `🌀 依赖地狱犬 DependencyHell` — 三头犬分别代表 pip/poetry/uv |
| **小怪清单** | `虚拟环境史莱姆` `pyproject.toml 石像` `pip 食人花` `async 元素精灵` `aiofiles 鹰身女妖` |
| **掉落装备** | ⚔️ uv 管理之剑 · 🛡️ 虚拟环境护盾 · 👢 asyncio 疾风靴 |
| **EXP** | ⭐⭐ (2/5) — 工程化概念对前端很友好 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ uv 管理项目 ✅ asyncio.gather 并发 ✅ httpx 异步客户端 |

### 🚀 Level 1-3：疾风 API · FastAPI 精通

| 属性 | 内容 |
|------|------|
| **BOSS** | `⚡ 路由九头蛇 RouteHydra` — 每砍掉一个路由就长出两个新端点 |
| **小怪清单** | `@decorator 蜘蛛` `Pydantic 魔像` `Depends 链魔` `Swagger 飞龙（友方）` `HTTPException 毒蝎` |
| **掉落装备** | ⚔️ FastAPI 疾风剑 · 🛡️ Pydantic 验证盾 · 📜 Swagger 自动文档卷轴 |
| **EXP** | ⭐⭐⭐ (3/5) — 框架学习需要适应 |
| **HP 消耗** | ~20h |
| **通关条件** | ✅ CRUD 端点 ✅ JWT 认证 ✅ pytest 测试 ✅ Swagger 可访问 |

### 🗄️ Level 1-4：数据掌控者 · SQLAlchemy + 项目交付

| 属性 | 内容 |
|------|------|
| **BOSS** | `🐉 异步魔龙 asyncio（区域BOSS）` — 多表联查攻击 + 迁移诅咒 |
| **小怪清单** | `ORM 石像鬼` `Session 幽灵` `Alembic 时光法师（友方）` `外键陷阱食人花` `pytest-asyncio 守卫` |
| **掉落装备** | 🗡️ SQLAlchemy 龙牙匕首 · 🛡️ Alembic 时光盾 · 🏆 **dev-note-api 神器** |
| **EXP** | ⭐⭐⭐ (3/5) — ORM 关系映射有学习曲线 |
| **HP 消耗** | ~20h |
| **通关条件** | ✅ 完整 CRUD + JWT ✅ Alembic 迁移 ✅ 12+ 测试 ✅ README |

---

## 🧠 阶段二：思维神殿 — LLM 基础原理

> **区域主题**：踏入 LLM 神殿，解开大模型的思维密码
> **区域 BOSS**：`👁️ Token 守护者 TokenGuardian` — 守护 LLM 核心秘密的神殿守卫
> **区域时间**：3 周 | **区域总 EXP**：15

```
🧠 思维神殿 · Lv.2-1 → Lv.2-2 → Lv.2-3
   🧠 思维觉醒  →  🔌 API召唤 →  🔍 代码审查

   BOSS: 🔮 注意力之眼   🌡️ 温控元素使   👁️ Token守护者(区域BOSS)
```

### 🧠 Level 2-1：思维觉醒 · 理解大模型

| 属性 | 内容 |
|------|------|
| **BOSS** | `🔮 注意力之眼 AttentionEye` — 让你理解模型如何「看」世界 |
| **小怪清单** | `Token 碎片魔` `Embedding 向量幽灵` `Transformer 巨石像` `Context Window 界限守卫` `Temperature 温控龙` |
| **掉落装备** | 🧠 Token 理解之冠 · 📐 Embedding 量尺 · 🗺️ 模型选型地图 |
| **EXP** | ⭐⭐ (2/5) — 概念理解为主，不涉及数学推导 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 解释 Token/Embedding/Attention ✅ 说出 4+ 模型特点 ✅ 画 LLM 流程图 |

### 🔌 Level 2-2：API 召唤师 · 调用大模型

| 属性 | 内容 |
|------|------|
| **BOSS** | `🌡️ 温控元素使 TemperatureElemental` — 用温度参数控制创造力的元素生物 |
| **小怪清单** | `API Key 钥匙妖精` `Stream 流水蛇` `Rate Limit 栅栏魔` `Message 三角幽灵 (system/user/assistant)` `Error Code 陷阱蜘蛛` |
| **掉落装备** | 🪄 OpenAI SDK 魔杖 · 📡 流式输出水晶球 · 🎛️ 多模型切换器 |
| **EXP** | ⭐⭐ (2/5) — API 调用对前端来说非常熟悉 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 调用 API ✅ 流式输出 ✅ temperature 实验 ✅ 错误处理 |

### 🔍 Level 2-3：代码审查官 · AI CR 工具

| 属性 | 内容 |
|------|------|
| **BOSS** | `👁️ Token 守护者 TokenGuardian（区域BOSS）` — 最终考验：用 AI 守护代码质量 |
| **小怪清单** | `System Prompt 工匠` `Git Diff 变形怪` `Rich 彩虹鸟（友方）` `Markdown 排版术士` `CLI 框架石像` |
| **掉落装备** | 🏆 **ai-code-review 神器** · 📝 代码审查之眼 · 🎨 Rich 彩虹终端 |
| **EXP** | ⭐⭐⭐ (3/5) — 首个完整的 LLM 应用项目 |
| **HP 消耗** | ~20h |
| **通关条件** | ✅ check + diff 模式 ✅ 等级分类 ✅ 修复建议 ✅ README |

---

## 📚 阶段三：知识深渊 — Prompt Engineering & RAG

> **区域主题**：潜入知识深渊，掌握 Prompt 魔法和 RAG 检索技艺
> **区域 BOSS**：`👻 幻觉幻影领主 HallucinationLord` — 制造虚假信息的幻影领主
> **区域时间**：4 周 | **区域总 EXP**：20

```
📚 知识深渊 · Lv.3-1 → Lv.3-2 → Lv.3-3 → Lv.3-4 → 🏕️ 补给站
   💬 低语智者  →  📚 知识编织 →  🔗 框架驾驭 →  🏗️ 文档智者

   BOSS: 🎭 人格面具   🧩 碎片魔像   ⚙️ 抽象魔偶   👻 幻觉幻影领主(区域BOSS)
```

### 💬 Level 3-1：低语智者 · Prompt 工程精通

| 属性 | 内容 |
|------|------|
| **BOSS** | `🎭 人格面具 PersonaMask` — 在不同 Prompt 策略间变换身份的诡术师 |
| **小怪清单** | `Zero-shot 空魔术士` `Few-shot 示例精灵` `CoT 思考链魔` `ToT 树形妖` `ReAct 循环守卫` `Self-Consistency 投票石像` |
| **掉落装备** | 📜 Prompt 模板集 · 🎭 人格面具 · 🔮 Jinja2 模板引擎 |
| **EXP** | ⭐⭐⭐ (3/5) — 7 种策略需要实验对比 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 区分 5+ Prompt 策略 ✅ Few-shot 示例 ✅ 结构化输出 ✅ 解释 ReAct |

### 📚 Level 3-2：知识编织者 · RAG 入门

| 属性 | 内容 |
|------|------|
| **BOSS** | `🧩 碎片魔像 ChunkGolem` — 由无数文档碎片组成的巨像，需要完美切分才能击败 |
| **小怪清单** | `Chunking 剪刀手` `Embedding 织网者` `Chroma 萤火虫（友方）` `MMR 检索妖精` `Metadata 过滤器` |
| **掉落装备** | 🗡️ Chunking 分割之刃 · 🛡️ Chroma 向量盾 · 🧭 相似度罗盘 |
| **EXP** | ⭐⭐⭐ (3/5) — RAG 流水线有多个环节 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 画 RAG 流程图 ✅ 选 Chunking 策略 ✅ Chroma 检索 ✅ 完整链路 |

### 🔗 Level 3-3：框架驾驭者 · LangChain & LlamaIndex

| 属性 | 内容 |
|------|------|
| **BOSS** | `⚙️ 抽象魔偶 AbstractionGolem` — LangChain 层层抽象组成的机械魔偶 |
| **小怪清单** | `LCEL 管道妖精` `ChainLink 锁链魔` `Retriever 猎犬` `LlamaIndex 巨鹰（友方）` `Ollama 雪人（可选）` |
| **掉落装备** | 🔗 LangChain 链刃 · 🦙 LlamaIndex 巨鹰坐骑 · 🧩 框架选型罗盘 |
| **EXP** | ⭐⭐⭐ (3/5) — 两个框架的 API 都需要熟悉 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ LCEL 链式调用 ✅ LlamaIndex 快速 RAG ✅ 框架定位差异 |

### 🏗️ Level 3-4：文档智者 · RAG 系统交付

| 属性 | 内容 |
|------|------|
| **BOSS** | `👻 幻觉幻影领主 HallucinationLord（区域BOSS）` — 虚假知识的制造者，用「不知道」护盾方可对抗 |
| **小怪清单** | `文档上传食人花` `流式输出水龙` `来源引用追踪者` `边界情况幽灵` `前端界面魅魔（可选）` |
| **掉落装备** | 🏆 **doc-qa 神器** · 👁️ 来源追溯之眼 · 🌊 流式回答波浪 |
| **EXP** | ⭐⭐⭐⭐ (4/5) — 完整的 RAG 系统是重要里程碑 |
| **HP 消耗** | ~20h |
| **通关条件** | ✅ 文档上传 ✅ 来源引用 ✅ 流式返回 ✅ 「不知道」处理 ✅ 响应<5s |

---

## 🤖 阶段四：机械王都 — AI Agent 框架

> **区域主题**：进入 Agent 的机械王都，组装你的智能体军团
> **区域 BOSS**：`🐲 状态机巨龙 StateMachineDragon` — 管理 Agent 复杂状态流转的远古巨龙
> **区域时间**：5 周 | **区域总 EXP**：25（最大区域）

```
🤖 机械王都 · Lv.4-1 → Lv.4-2 → Lv.4-3 → Lv.4-4 → Lv.4-5
   🤖 智能觉醒  →  🔀 图灵绘师 →  🛠️ 装备大师 →  🎭 多面手  →  🏢 客服帝国

   BOSS: 🔄 ReAct巨兽   🌳 图灵织网者  💭 记忆吞噬者  👥 五头协调兽  🐲 状态机巨龙(区域BOSS)
```

### 🤖 Level 4-1：智能体觉醒 · Agent 基础

| 属性 | 内容 |
|------|------|
| **BOSS** | `🔄 ReAct 循环巨兽 ReActCyclops` — 不停执行 Thought→Action→Observation 的独眼巨人 |
| **小怪清单** | `Agent 自主魔偶` `Tool 工具妖精` `Planning 规划法师` `Memory 记忆幽灵` `Function Calling 石像` |
| **掉落装备** | 🤖 Agent 核心芯片 · 🔧 Tool 工具腰带 · 🔄 ReAct 循环引擎 |
| **EXP** | ⭐⭐⭐ (3/5) — Agent 是一个思维范式转变 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ Agent 四大组件 ✅ ReAct 流程图 ✅ Tool 定义 ✅ 决策链观察 |

### 🔀 Level 4-2：图灵绘师 · LangGraph 工作流

| 属性 | 内容 |
|------|------|
| **BOSS** | `🌳 图灵织网者 GraphWeaver` — 用节点和边编织命运的蛛网领主 |
| **小怪清单** | `StateGraph 魔方` `Node 守卫` `ConditionalEdge 岔路妖` `Checkpoint 存档精灵（友方）` `interrupt 时停术士` |
| **掉落装备** | 🗺️ StateGraph 地图 · 🔀 条件路由罗盘 · 💾 Checkpoint 存档水晶 |
| **EXP** | ⭐⭐⭐⭐ (4/5) — LangGraph 是核心技能 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ StateGraph 定义 ✅ 条件路由 ✅ Checkpoint 恢复 ✅ HITL 审批 |

### 🛠️ Level 4-3：装备大师 · Tool 与 Memory

| 属性 | 内容 |
|------|------|
| **BOSS** | `💭 记忆吞噬者 MemoryDevourer` — 吞噬对话历史、超出 Context Window 的记忆巨兽 |
| **小怪清单** | `Tool Registry 铁匠` `BufferMemory 缓冲魔` `SummaryMemory 压缩法师` `Token-aware 剪刀手` `Reducer 锁链` |
| **掉落装备** | 🛠️ Tool 锻造锤 · 💭 双记忆护盾（短期+长期）· ✂️ 记忆裁剪剪刀 |
| **EXP** | ⭐⭐⭐ (3/5) — Tool 和 Memory 是 Agent 的双手和大脑 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 参数验证 Tool ✅ 短期+长期记忆 ✅ Token 预算管理 |

### 🎭 Level 4-4：多面手联盟 · Multi-Agent 编排

| 属性 | 内容 |
|------|------|
| **BOSS** | `👥 五头协调兽 PentCoordinator` — 五个头分别使用 Router/Sequential/Debate/Hierarchical/Parallel 模式 |
| **小怪清单** | `CrewAI 船员妖精` `AutoGen 对话傀儡` `Debate 辩论骑士` `Parallel 分身术士` `Merge 融合法师` |
| **掉落装备** | 👥 Multi-Agent 指挥旗 · 🎭 CrewAI 角色面具 · ⚔️ AutoGen 代码之刃 |
| **EXP** | ⭐⭐⭐⭐ (4/5) — 多 Agent 是进阶能力 |
| **HP 消耗** | ~18h |
| **通关条件** | ✅ 5 种模式架构图 ✅ LangGraph 2 种模式 ✅ 框架选型 |

### 🏢 Level 4-5：客服帝国 · 项目交付

| 属性 | 内容 |
|------|------|
| **BOSS** | `🐲 状态机巨龙 StateMachineDragon（区域BOSS）` — 管理 4 个 Agent 复杂状态流转的远古巨龙 |
| **小怪清单** | `Router 守卫` `Knowledge RAG 龙` `Ticket 工单兽` `Summarize 压缩鸟` `Checkpoint 存档祭司` |
| **掉落装备** | 🏆 **agent-support 神器** · 🏰 Multi-Agent 城堡 · 🌐 WebSocket 传送门 |
| **EXP** | ⭐⭐⭐⭐⭐ (5/5) — 整个路线中最核心的项目 |
| **HP 消耗** | ~20h |
| **通关条件** | ✅ Router 3 意图 ✅ Knowledge 准确回答 ✅ Ticket 创建工单 ✅ Summarize 摘要 ✅ Checkpoint 恢复 |

---

## 📡 阶段五：协议