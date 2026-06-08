import subprocess
from langchain_core.tools import tool
import paramiko
from pydantic import BaseModel, Field

@tool
def get_kubernetes_pod_logs(pod_name: str) -> str:
    """Sử dụng công cụ này để lấy log của một Pod cụ thể trong Kubernetes khi Pod đó bị lỗi."""
    # TRONG THỰC TẾ: Bạn sẽ chạy lệnh k8s thật như sau:
    # result = subprocess.run(["kubectl", "logs", pod_name, "--tail=20"], capture_output=True, text=True)
    # return result.stdout if result.returncode == 0 else result.stderr
    
    # MÔ PHỎNG: Để bạn có thể test code ngay trên máy cá nhân không có K8s
    if "nginx" in pod_name.lower():
        return "[ERROR] 2026-06-01 15:00:05: OOMKilled. Memory limit exceeded. Resource configuration: limits.memory=128Mi"
    elif "db" in pod_name.lower():
        return "[FATAL] Connection refused to database port 5432. Too many open connections."
    else:
        return f"Pod {pod_name} found, but logs are clean or pod is starting."

class SSHCommandInput(BaseModel):
    server_ip: str = Field(description="Địa chỉ IP hoặc Hostname của server đích cần chạy lệnh.")
    command: str = Field(description="Lệnh Linux cụ thể cần thực thi (ví dụ: 'df -h', 'uptime', 'systemctl status nginx').")

@tool("run_remote_command", args_schema=SSHCommandInput)
def run_remote_command(server_ip: str, command: str) -> str:
    """
    Thực thi một lệnh Linux trên một server cụ thể thông qua SSH và trả về kết quả (stdout/stderr).
    Hãy sử dụng công cụ này khi người dùng yêu cầu chạy lệnh hoặc kiểm tra trạng thái trên một server từ xa.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Cấu hình thông tin SSH (Trong thực tế, bạn nên lấy từ biến môi trường hoặc Secret Manager)
    ssh_user = "your_ssh_username" 
    ssh_password = "your_ssh_password" # Hoặc dùng ssh.connect(..., key_filename="path/to/key")
    
    try:
        # Thực hiện kết nối SSH
        ssh.connect(hostname=server_ip, username=ssh_user, password=ssh_password, timeout=10)
        
        # Chạy lệnh
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error:
            return f"Lỗi khi chạy lệnh trên {server_ip}:\n{error}"
        return f"Kết quả lệnh từ server {server_ip}:\n{output}"
        
    except Exception as e:
        return f"Không thể kết nối đến server {server_ip} qua SSH. Chi tiết lỗi: {str(e)}"
    finally:
        ssh.close()