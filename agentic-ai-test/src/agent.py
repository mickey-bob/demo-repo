# --- PHẦN IMPORT Ở ĐẦU FILE ---
import os
import sqlite3
from dotenv import load_dotenv
from langchain_ollama import ChatOllama 
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
# from langgraph.checkpoint.sqlite import SqliteSaver

# Đảm bảo bạn đã ĐỔI dòng import này:
from langgraph.checkpoint.memory import MemorySaver

from src.tools import get_kubernetes_pod_logs, run_remote_command

load_dotenv()

def create_devops_agent():
    # 2. Khởi tạo Llama 3.2 thông qua Ollama
    # Chúng a truyền vào url lấy từ file .env
    model = ChatOllama(
        model="llama3.2", 
        temperature=0,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    
    # 3. Danh sách công cụ (Giữ nguyên)
    tools = [get_kubernetes_pod_logs, run_remote_command]
    
    # 4. System Prompt (Giữ nguyên)
    system_prompt = SystemMessage(
        content="Bạn là một chuyên gia DevOps kiêm SRE lão luyện. Nhiệm vụ của bạn là hỗ trợ phân tích sự cố hạ tầng. "
                "Hãy luôn sử dụng công cụ để lấy log thực tế trước khi đưa ra kết luận. "
                "Sau khi phân tích log, hãy giải thích nguyên nhân và đề xuất giải pháp sửa lỗi."
    )
    
    # 5. Khởi tạo Database SQLite làm ký ức (Giữ nguyên)
    os.makedirs("data", exist_ok=True)
    # conn = sqlite3.connect("data/agent_memory.db", check_same_thread=False)
    memory = MemorySaver()
    # memory = SqliteSaver(conn)
    
    # 6. Tạo Agent (Giữ nguyên cấu trúc LangGraph)
    agent_executor = create_react_agent(
        model, 
        tools=tools, 
        prompt=system_prompt,
        checkpointer=memory
    )
    return agent_executor