# 智能电商客服系统（Ecommerce Customer Service）

基于大模型（LLM）的智能电商客服系统。前端提供带数字人形象的客服聊天工作台，客服后端内置对话引擎，通过 YAML 流程编排驱动任务型对话，可对接真实电商业务服务完成订单查询、物流追踪、退款申请、相似商品推荐等操作。

## 系统架构

```
┌──────────────────────────────────┐
│  customer-service-frontend       │  Vue 3 + Vite
│  客服聊天工作台 / 数字人面板       │  http://127.0.0.1:5173
└───────────┬──────────┬───────────┘
       /api │          │ /commerce
            ▼          ▼
┌───────────────────────┐   HTTP    ┌────────────────────────────┐
│ customer-service-     │──────────▶│ ecommerce-service-backend  │
│ backend (FastAPI)     │           │ 电商业务服务 (FastAPI)       │
│ 对话引擎 / 流程编排     │           │ http://127.0.0.1:18081     │
│ http://127.0.0.1:18082│           └─────────────┬──────────────┘
└──────────┬────────────┘                         │
           │            LLM (OpenAI 兼容接口)      │
           │◀─────────────────────┐               │
           ▼                      ▼               ▼
┌─────────────────────────────────────────────────────────┐
│              MySQL 8.4（Docker, 端口 3308）               │
│  customer_service 库：对话状态       commerce 库：电商业务数据 │
└─────────────────────────────────────────────────────────┘
```

## 目录结构

```
.
├── customer-service-frontend/        # 前端：Vue 3 + Vite 客服工作台
│   └── src/
│       ├── App.vue                   # 聊天主界面（订单/商品侧边栏）
│       └── DigitalPersonPanel.vue    # 数字人面板
├── customer-service-backend/         # 客服后端：FastAPI + LangChain
│   ├── main.py                       # 启动入口（:18082）
│   ├── pyproject.toml / uv.lock      # 依赖管理（uv）
│   ├── .env                          # 环境变量（LLM、数据库等）
│   ├── flowConfig/                   # YAML 流程编排配置
│   │   ├── system_flows.yml          # 系统级流程（任务开始/恢复/无法处理等）
│   │   └── user_flows.yml            # 业务流程（订单、物流、退款等）
│   └── atguigu/                      # 业务代码包
│       ├── api/                      # REST / WebSocket 接口层
│       ├── engine/                   # 对话引擎（DialogueEngine）
│       ├── plan/                     # 轮次规划与校验（TurnPlanner）
│       ├── task/                     # 任务处理：flow / action / commands
│       ├── knowledge/                # 知识问答处理
│       ├── chitchat/                 # 闲聊处理
│       ├── clarify/                  # 澄清追问
│       ├── prompt/                   # Prompt 加载（Jinja2 模板）
│       ├── domain/                   # 领域模型（消息、状态、上下文）
│       ├── repository/               # 对话状态持久化
│       ├── infrastructure/           # 数据库 / HTTP / LLM 客户端
│       ├── service/                  # 对话服务、历史服务
│       └── test/                     # 独立测试脚本
├── ecommerce-service-backend/        # 电商业务服务：FastAPI（:18081）
│   ├── main.py
│   └── app/                          # 订单 / 物流 / 商品 / 退款等接口
└── docker/                           # 基础设施
    ├── docker-compose.yml            # MySQL 8.4（端口 3308）
    └── mysql/initdb/                 # 建库、建表与示例数据初始化脚本
```

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 客服后端 | Python 3.12+、FastAPI、LangChain / langchain-openai、SQLAlchemy（aiomysql 异步驱动）、Pydantic Settings、uv |
| 电商业务服务 | Python 3.12+、FastAPI、SQLAlchemy（pymysql）、uv |
| 前端 | Vue 3、Vite 6 |
| 数据库 | MySQL 8.4（Docker Compose） |
| 实时通信 | WebSocket |

## 核心功能

- **对话引擎**：`DialogueEngine` 按轮次调度任务处理（TaskHandler）、知识问答（KnowledgeHandler）、闲聊（ChitchatHandler），并配合轮次规划（TurnPlanner）、计划校验与澄清追问（Clarify）完成多轮对话。
- **流程编排**：以 YAML 定义对话流程（`flowConfig/*.yml`），支持条件分支与动作节点，内置业务流程包括：
  - `onboarding` 打招呼与能力介绍
  - `order_status_query` 订单状态查询
  - `logistics_tracking` 物流轨迹查询
  - `refund_request` 退款申请
  - `similar_product_recommendation` 相似商品推荐
  - `human_handoff` 转人工
- **可扩展 Action**：`task/action/builtin`（`action_listen`、`action_response`）与 `task/action/custom`（查订单状态、查物流、推荐相似商品、提交退款申请），通过注册机制扩展。
- **接口形式**：
  - `POST /api/chat`：同步对话接口
  - `WS /ws/chat`：WebSocket 实时对话（`thinking` / `bot_message` / `status` 状态帧）
  - `GET /api/chat/history`：聊天历史
  - `GET /api/digital-human/credentials`：数字人凭证
- **电商业务服务**：用户订单/商品列表、订单详情与状态、物流查询、商品详情、创建发货提醒、提交退款申请，初始化数据覆盖待发货、运输中、已完成、已取消等多种状态。
- **前端工作台**：聊天窗口 + 订单/商品侧边栏 + 数字人形象面板，默认演示用户 `u1001`。

## 快速开始

### 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)（Python 依赖管理）
- Node.js 18+
- Docker + Docker Compose

### 1. 启动 MySQL

```bash
cd docker
docker compose up -d
```

- 端口：`3308`（容器内 3306）
- 用户/密码：`atguigu` / `Atguigu.123`
- 首次启动自动执行 `mysql/initdb/` 下的初始化脚本，创建 `customer_service`（对话状态）与 `commerce`（电商业务示例数据）两个库。

> 如需重置数据：`docker compose down -v` 后再 `docker compose up -d`。

### 2. 启动客服后端（:18082）

```bash
cd customer-service-backend
uv sync
PYTHONPATH=".;./atguigu" uv run main.py
```

Windows PowerShell：

```powershell
cd customer-service-backend
uv sync
$env:PYTHONPATH=".;./atguigu"; uv run main.py
```

> 项目已附带 `.env` 演示配置，可按需修改（见下方「环境变量」）。
> 接口文档：http://127.0.0.1:18082/docs

### 3. 启动电商业务服务（:18081）

```bash
cd ecommerce-service-backend
uv sync
uv run main.py
```

> 默认连接 `mysql+pymysql://atguigu:Atguigu.123@127.0.0.1:3308/commerce`，与 Docker 初始化数据一致。
> 接口文档：http://127.0.0.1:18081/docs

### 4. 启动前端（:5173）

```bash
cd customer-service-frontend
npm install
npm run dev
```

浏览器访问 http://127.0.0.1:5173，即可与客服助手对话。开发服务器已配置代理：

- `/api` → `http://127.0.0.1:18082`（客服后端）
- `/commerce` → `http://127.0.0.1:18081`（电商业务服务）

## 环境变量

客服后端读取 `customer-service-backend/.env`：

| 变量 | 说明 |
| --- | --- |
| `LLM_MODEL` | 模型名称（OpenAI 兼容接口） |
| `LLM_BASE_URL` | LLM API 地址 |
| `LLM_API_KEY` | LLM API Key |
| `DATABASE_URL` | 客服后端数据库连接串（`customer_service` 库） |
| `COMMERCE_API_BASE_URL` | 电商业务服务地址，默认 `http://127.0.0.1:18081` |
| `APP_HOST` / `APP_PORT` | 客服后端监听地址与端口（默认 `18082`） |
| `DIGITAL_HUMAN_APP_ID` / `DIGITAL_HUMAN_APP_SECRET` | 数字人服务凭证 |

电商业务服务通过环境变量覆盖默认值：`DATABASE_URL`、`APP_HOST`、`APP_PORT`（默认 `18081`）。

## 主要接口

### 客服后端（:18082）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/chat/history?sender_id=` | 查询聊天历史 |
| POST | `/api/chat` | 同步对话 |
| WS | `/ws/chat` | WebSocket 实时对话 |
| GET | `/api/digital-human/credentials` | 获取数字人凭证 |

### 电商业务服务（:18081）

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查 |
| GET | `/users/{user_id}/orders` | 用户订单列表 |
| GET | `/users/{user_id}/products` | 用户商品列表 |
| GET | `/orders/{order_id}` | 订单详情 |
| GET | `/orders/{order_id}/status` | 订单状态 |
| GET | `/orders/{order_id}/logistics` | 订单物流 |
| GET | `/products/{product_id}` | 商品详情 |
| POST | `/orders/{order_id}/shipping-reminders` | 创建发货提醒 |
| POST | `/orders/{order_id}/refund-applications` | 提交退款申请 |

## 测试

`customer-service-backend/atguigu/test/` 下为独立测试脚本（数据库、HTTP 客户端、LLM 客户端、流程加载、仓储等），示例：

```bash
cd customer-service-backend
PYTHONPATH=".;./atguigu" uv run python atguigu/test/test_load_flow.py
```
