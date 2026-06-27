## 项目启动步骤
+ 启动`postgresql`数据库
```bash
pg_ctl -D $HOME/postgresql/data start
```
+ 激活`venv`环境
```bash
source venv/bin/activate
```
+ 启动项目后端服务
```bash
cd backend
```
```bash
poetry run uvicorn app.main:app --reload
```
+ 启动项目前端服务
```bash
cd frontend
```
```bash
npm run dev
```

## AI Agent Intelligence Site

This demo now includes a public AI Agent intelligence site.

Backend:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Seed demo content:

```bash
curl -X POST http://127.0.0.1:8000/api/intelligence/seed
curl http://127.0.0.1:8000/api/intelligence/home
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173/` to view the public site.

Admin pages are still available under `/admin`, for example `http://127.0.0.1:5173/admin/home`.

The first MVP keeps local notes private unless a Markdown file contains:

```yaml
---
publish: true
---
```
