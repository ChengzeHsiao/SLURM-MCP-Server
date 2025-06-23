from mcp.server import FastMCP

app = FastMCP('slurm-mcp-server')

@app.tool()
async def get_slurm_jobs() -> str:
    """
    获取 SLURM 作业列表。

    Returns:
        SLURM 作业列表的字符串表示。
    """
    import subprocess
    result = subprocess.run(['squeue', '-h'], capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def query_slurm_job(job_id: str) -> str:
    """
    查询特定 SLURM 任务的执行状态。

    Args:
        job_id: 要查询的作业 ID。

    Returns:
        指定作业的详细状态信息。
    """
    import subprocess
    result = subprocess.run(['squeue', '-j', job_id], capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def submit_slurm_job(script_content: str, job_name: str = "mcp_job") -> str:
    """
    提交新的 SLURM 任务。

    Args:
        script_content: 任务脚本的内容。
        job_name: 任务的名称，默认为 "mcp_job"。

    Returns:
        提交任务的结果，包含作业 ID 或错误信息。
    """
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(script_content)
        script_path = f.name
    result = subprocess.run(['sbatch', '--job-name', job_name, script_path], capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def cancel_slurm_job(job_id: str) -> str:
    """
    取消指定的 SLURM 任务。

    Args:
        job_id: 要取消的作业 ID。

    Returns:
        取消操作的结果。
    """
    import subprocess
    result = subprocess.run(['scancel', job_id], capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def get_slurm_job_history(user: str = None, status: str = None) -> str:
    """
    查询 SLURM 历史任务。

    Args:
        user: 可选，按用户过滤历史任务。
        status: 可选，按任务状态（如 COMPLETED, FAILED）过滤历史任务。

    Returns:
        符合条件的 SLURM 历史任务列表。
    """
    import subprocess
    cmd = ['sacct', '-P', '-o', 'JobID,JobName,User,State,Elapsed']
    if user: cmd.extend(['--user', user])
    if status: cmd.extend(['--state', status])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def get_slurm_nodes_info() -> str:
    """
    获取 SLURM 集群中节点的信息。

    Returns:
        SLURM 节点信息的字符串表示。
    """
    import subprocess
    result = subprocess.run(['sinfo', '-Nl'], capture_output=True, text=True, check=True)
    return result.stdout

@app.tool()
async def get_slurm_partitions_info() -> str:
    """
    获取 SLURM 集群中分区的信息。

    Returns:
        SLURM 分区信息的字符串表示。
    """
    import subprocess
    result = subprocess.run(['sinfo'], capture_output=True, text=True, check=True)
    return result.stdout


def main():
    app.settings.host = "0.0.0.0"
    app.settings.port = 8000
    app.run(transport="sse")


if __name__ == "__main__":
    main()

