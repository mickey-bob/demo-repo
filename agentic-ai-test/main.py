from src.agent import create_devops_agent

def main():
    agent = create_devops_agent()
    
    # Cấu hình Session ID (Thread ID). 
    # Mọi trạng thái của cuộc đối thoại này sẽ được lưu vào SQLite gắn với ID này.
    config = {"configurable": {"thread_id": "devops_incident_session_001"}}
    
    print("🤖 Agentic DevOps sẵn sàng! (Gõ 'exit' để thoát)\n" + "-"*50)
    
    # LƯỢT 1: Bạn ra lệnh cho Agent kiểm tra lỗi
    # user_input_1 = "Pod nginx-web-7fd4 của tôi đang bị Crash. Hãy check log và phân tích giúp tôi."
    user_input_1 = "kiểm tra disk usage trên server: 192.168.10.133"
    print(f"👤 User: {user_input_1}\n")
    
    # Chạy agent
    events = agent.stream({"messages": [("user", user_input_1)]}, config, stream_mode="values")
    for event in events:
        # Lấy tin nhắn cuối cùng trong chuỗi hành động của Agent để in ra
        final_message = event["messages"][-1]
    print(f"🤖 Agent:\n{final_message.content}\n" + "-"*50)
    
    # LƯỢT 2: Bạn hỏi một câu không hề nhắc lại tên Pod (Test tính Stateful)
    user_input_2 = "Thế còn phương án xử lý ngắn hạn và dài hạn cho lỗi tôi vừa hỏi ở trên là gì?"
    print(f"👤 User: {user_input_2}\n")
    
    events = agent.stream({"messages": [("user", user_input_2)]}, config, stream_mode="values")
    for event in events:
        final_message = event["messages"][-1]
    print(f"🤖 Agent:\n{final_message.content}\n" + "-"*50)

if __name__ == "__main__":
    main()