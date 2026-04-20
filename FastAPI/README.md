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
