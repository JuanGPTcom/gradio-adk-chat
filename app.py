import gradio as gr
import requests
import json
import os
from typing import List, Tuple, Optional

class ADKChatClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the ADK chat client"""
        self.api_key = api_key or os.getenv("GOOGLE_ADK_API_KEY")
        self.base_url = base_url or "https://generativelanguage.googleapis.com/v1beta"
        self.session_id = None
        
    def start_session(self, agent_id: str) -> bool:
        """Start a new chat session with an ADK agent"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "agent_id": agent_id,
                "session_config": {
                    "enable_streaming": True,
                    "max_turns": 50
                }
            }
            
            response = requests.post(
                f"{self.base_url}/sessions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                self.session_id = response.json().get("session_id")
                return True
            else:
                print(f"Failed to start session: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error starting session: {str(e)}")
            return False
    
    def send_message(self, message: str) -> Optional[str]:
        """Send a message to the ADK agent and get response"""
        if not self.session_id:
            return "Error: No active session. Please start a session first."
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "message": {
                    "content": message,
                    "type": "text"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/sessions/{self.session_id}/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json().get("response", {}).get("content", "No response received")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error sending message: {str(e)}"
    
    def end_session(self):
        """End the current chat session"""
        if self.session_id:
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                requests.delete(f"{self.base_url}/sessions/{self.session_id}", headers=headers)
                self.session_id = None
            except:
                pass

# Global client instance
adk_client = ADKChatClient()

def setup_agent(api_key: str, agent_id: str) -> str:
    """Setup the ADK agent connection"""
    if not api_key:
        return "Please enter your Google ADK API key"
    
    if not agent_id:
        return "Please enter an Agent ID"
    
    global adk_client
    adk_client = ADKChatClient(api_key=api_key)
    
    if adk_client.start_session(agent_id):
        return f"? Successfully connected to agent: {agent_id}"
    else:
        return "? Failed to connect to agent. Check your API key and Agent ID."

def chat_with_agent(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """Handle chat interaction with the ADK agent"""
    if not message.strip():
        return "", history
    
    if not adk_client.session_id:
        return "", history + [(message, "Please setup the agent connection first using the Setup tab.")]
    
    # Get response from ADK agent
    response = adk_client.send_message(message)
    
    # Update history
    history.append((message, response))
    
    return "", history

def clear_chat():
    """Clear the chat history"""
    return []

def disconnect_agent():
    """Disconnect from the current agent"""
    global adk_client
    adk_client.end_session()
    return "Disconnected from agent"

# Create the Gradio interface
with gr.Blocks(title="ADK Agent Chat", theme=gr.themes.Soft()) as app:
    gr.Markdown("# ? Google ADK Agent Chat")
    gr.Markdown("Connect and chat with AI agents using Google's Agent Development Kit protocol")
    
    with gr.Tabs():
        # Setup Tab
        with gr.Tab("Setup"):
            gr.Markdown("### Configure Your ADK Agent Connection")
            
            with gr.Row():
                api_key_input = gr.Textbox(
                    label="Google ADK API Key",
                    type="password",
                    placeholder="Enter your Google ADK API key...",
                    scale=2
                )
                agent_id_input = gr.Textbox(
                    label="Agent ID",
                    placeholder="Enter the agent ID to connect to...",
                    scale=1
                )
            
            setup_btn = gr.Button("Connect to Agent", variant="primary")
            setup_status = gr.Textbox(label="Connection Status", interactive=False)
            
            setup_btn.click(
                fn=setup_agent,
                inputs=[api_key_input, agent_id_input],
                outputs=setup_status
            )
            
            gr.Markdown("""
            ### How to get started:
            1. Get your Google ADK API key from the Google Cloud Console
            2. Create or identify an agent ID from your ADK project
            3. Enter both values above and click "Connect to Agent"
            4. Switch to the Chat tab to start conversing
            """)
        
        # Chat Tab
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(
                label="ADK Agent Conversation",
                height=500,
                show_copy_button=True
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    label="Message",
                    placeholder="Type your message to the agent...",
                    scale=4,
                    show_label=False
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
                disconnect_btn = gr.Button("Disconnect Agent", variant="stop")
            
            disconnect_status = gr.Textbox(label="Status", interactive=False, visible=False)
            
            # Event handlers
            send_btn.click(
                fn=chat_with_agent,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )
            
            msg_input.submit(
                fn=chat_with_agent,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot]
            )
            
            clear_btn.click(
                fn=clear_chat,
                outputs=chatbot
            )
            
            disconnect_btn.click(
                fn=disconnect_agent,
                outputs=disconnect_status
            ).then(
                lambda: gr.update(visible=True),
                outputs=disconnect_status
            ).then(
                lambda: gr.update(visible=False),
                outputs=disconnect_status,
                _js="() => setTimeout(() => {}, 2000)"
            )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )