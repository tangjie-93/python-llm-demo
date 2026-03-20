## 1. 创建 Python 虚拟环境

```bash
python -m venv venv
// 激活虚拟环境 linux/mac
source venv/bin/activate
// 激活虚拟环境 windows(powershell)
. venv/Scripts/activate 
```

***

## 2. 命令解析

### 2.1 `python -m venv venv`

| 部分       | 含义                    |
| -------- | --------------------- |
| `python` | 调用 `Python` 解释器       |
| `-m`     | 表示以模块方式运行（`module`）   |
| `venv`   | `Python` 内置的虚拟环境模块    |
| `venv`   | 虚拟环境的目录名称（第二个 `venv`） |

**完整含义**：使用 `Python` 的 `venv` 模块创建一个名为 `venv` 的虚拟环境目录。

> 注意：第二个 `venv` 是目录名，你可以改成其他名字，比如 `python -m venv myenv`

### 2.2 `source venv/bin/activate`

| 部分                  | 含义                      |
| ------------------- | ----------------------- |
| `source`            | `Shell` 命令，用于执行指定文件中的命令 |
| `venv/bin/activate` | 虚拟环境激活脚本的路径             |

**完整含义**：执行虚拟环境中的激活脚本，将当前 `shell` 会话切换到虚拟环境中。

***

## 3. 激活后的效果

激活成功后，你的命令行提示符前面会出现 `(venv)` 标识：

```bash
(venv) ➜  python-demo
```

这表示你现在处于虚拟环境中，此时：

- `python` 命令指向虚拟环境中的 `Python` 解释器
- `pip` 安装的包会被安装到虚拟环境中，而不是系统环境

***

## 4. 退出虚拟环境

当你想退出虚拟环境时，运行：

```bash
deactivate
```

***

## 5. 完整流程示例

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
// 激活虚拟环境 linux/mac
source venv/bin/activate
// 激活虚拟环境 windows
. venv\Scripts\activate 

# 3. 安装需要的包
pip install requests

# 4. 退出虚拟环境
deactivate
```

