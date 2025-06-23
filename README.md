# SLURM 任务管理 MCP 服务器

`slurm_mcp_server.py` 是一个基于 `FastMCP` 框架开发的 SLURM 任务管理服务器。它提供了一系列 API 工具，用于远程管理 SLURM 集群中的作业、查询节点和分区信息。

## 功能

该服务器提供了以下 SLURM 任务管理功能：

- **获取 SLURM 作业列表**：查询当前运行的 SLURM 作业。
- **查询特定 SLURM 任务状态**：根据作业 ID 查询详细状态。
- **提交新的 SLURM 任务**：提交 SLURM 脚本以运行新作业。
- **取消指定的 SLURM 任务**：根据作业 ID 取消正在运行的作业。
- **查询 SLURM 历史任务**：根据用户和状态过滤查询历史作业。
- **获取 SLURM 集群节点信息**：查询集群中所有节点的信息。
- **获取 SLURM 集群分区信息**：查询集群中所有分区的信息。
- **采用 MCP SSE 服务类型**：MCP Client 配置为 SSE 服务类型。

## 效果
![image](https://github.com/user-attachments/assets/e6a41dcf-cecd-42b0-aee1-35bf1bd1a268)

![image](https://github.com/user-attachments/assets/8af59e42-a4ba-4611-a2df-9c451cd83574)

## 安装

1. **推荐运行环境**：

   在SLURM Login\SLURM Haed 节点运行，推荐在 Haed节点运行。
   
3. **克隆仓库**：

   ```bash
   git clone https://github.com/ChengzeHsiao/SLURM-MCP-Server.git
   cd SLURM-MCP-Server
   ```

4. **创建并激活虚拟环境**：

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **安装依赖**：

   ```bash
   pip install -r requirements.txt # 如果有 requirements.txt
   # 或者手动安装 FastMCP
   pip install fastmcp
   ```

## 使用方法

1. **启动服务器**：

   ```bash
   python3 slurm_mcp_server.py
   # 或者后台运行
   nohup python3 slurm_mcp_server.py &
   ```

   服务器将默认在 `http://0.0.0.0:8000` 启动。

2. **通过 API 调用**：

   您可以使用任何 HTTP 客户端（如 `curl`、`requests` 库）或 MCP 客户端与服务器进行交互。以下是一些示例 API 调用：

   - **获取 SLURM 作业列表**：

     ```bash
     curl -X POST http://localhost:8000/tool/get_slurm_jobs -H "Content-Type: application/json" -d '{}'
     ```

   - **提交 SLURM 作业**：

     ```bash
     curl -X POST http://localhost:8000/tool/submit_slurm_job -H "Content-Type: application/json" -d '{"script_content": "#!/bin/bash\n#SBATCH --job-name=my_test_job\n#SBATCH --time=00:01:00\n#SBATCH --nodes=1\n\necho \"Hello from SLURM!\""}'
     ```

   - **取消 SLURM 作业**：

     ```bash
     curl -X POST http://localhost:8000/tool/cancel_slurm_job -H "Content-Type: application/json" -d '{"job_id": "<your-job-id>"}'
     ```

## API 工具列表

以下是 `slurm_mcp_server.py` 中提供的所有 API 工具及其功能：

- `get_slurm_jobs()`: 获取 SLURM 作业列表。
- `query_slurm_job(job_id: str)`: 查询特定 SLURM 任务的执行状态。
- `submit_slurm_job(script_content: str, job_name: str = "mcp_job")`: 提交新的 SLURM 任务。
- `cancel_slurm_job(job_id: str)`: 取消指定的 SLURM 任务。
- `get_slurm_job_history(user: str = None, status: str = None)`: 查询 SLURM 历史任务。
- `get_slurm_nodes_info()`: 获取 SLURM 集群中节点的信息。
- `get_slurm_partitions_info()`: 获取 SLURM 集群中分区的信息。

每个工具都通过 HTTP POST 请求调用，请求体为 JSON 格式，包含相应的参数。
