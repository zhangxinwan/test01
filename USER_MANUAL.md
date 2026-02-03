# 简单用户管理系统 使用说明

环境要求
- Python 3.8+

安装依赖
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

运行应用
```bash
python app.py
```

API 示例（在本地运行后，默认端口 5000）

- 列表用户
```bash
curl -s http://localhost:5000/users
```

- 创建用户
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}' http://localhost:5000/users
```

- 获取用户
```bash
curl http://localhost:5000/users/1
```

- 更新用户
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Alice B"}' http://localhost:5000/users/1
```

- 删除用户
```bash
curl -X DELETE http://localhost:5000/users/1
```

备注
- 数据库为 SQLite 文件 `users.db`，位于项目根目录。
- 可扩展点：添加分页、验证、认证（JWT）、单元测试等。
