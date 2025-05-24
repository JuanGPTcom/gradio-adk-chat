# Gradio ADK Chat

A simple, complete Gradio app for chatting with AI agents using Google's Agent Development Kit (ADK) protocol.

## Features

- ? **Simple Setup**: Just enter your API key and agent ID
- ? **Clean Chat Interface**: Standard chatbot UI with message history
- ? **Session Management**: Proper connection handling and cleanup
- ? **Docker Ready**: Easy deployment with Docker
- ?? **Error Handling**: Clear feedback for connection issues

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JuanGPTcom/gradio-adk-chat.git
   cd gradio-adk-chat
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python app.py
   ```

4. **Open your browser**: Go to `http://localhost:7860`

### Docker (Recommended)

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**:
   ```bash
   docker build -t gradio-adk-chat .
   docker run -p 7860:7860 gradio-adk-chat
   ```

## Configuration

### Environment Variables

- `GOOGLE_ADK_API_KEY`: Your Google ADK API key (optional, can be entered in UI)

### Setup Your Credentials

1. **Get Google ADK API Key**:
   - Go to Google Cloud Console
   - Enable the ADK API
   - Create credentials

2. **Get Agent ID**:
   - From your ADK project
   - Use the agent ID you want to chat with

## Usage

1. **Setup Tab**:
   - Enter your Google ADK API key
   - Enter the agent ID you want to connect to
   - Click "Connect to Agent"

2. **Chat Tab**:
   - Start conversing with your ADK agent
   - Use "Clear Chat" to reset conversation
   - Use "Disconnect Agent" to end session

## API Integration

The app uses Google's ADK protocol with the following endpoints:
- `POST /sessions` - Start a new chat session
- `POST /sessions/{session_id}/messages` - Send messages
- `DELETE /sessions/{session_id}` - End session

## Development

### Project Structure
```
.
??? app.py                 # Main Gradio application
??? requirements.txt       # Python dependencies
??? Dockerfile            # Docker container config
??? docker-compose.yml    # Docker Compose config
??? .env.example         # Environment variables template
??? README.md            # This file
```

### Adding Features

The `ADKChatClient` class handles all ADK protocol interactions. To add features:
1. Extend the client class with new methods
2. Add corresponding UI elements in the Gradio interface
3. Wire up event handlers

## Deployment

### Local Docker
```bash
docker-compose up -d
```

### Cloud Deployment
This app is ready for deployment on:
- Hugging Face Spaces
- Google Cloud Run
- AWS ECS
- Any Docker-compatible platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

MIT License - feel free to use this for your projects!

## Support

If you encounter issues:
1. Check your API key and agent ID
2. Verify your ADK project setup
3. Check Docker logs: `docker-compose logs`
4. Open an issue on GitHub

---

**Ready to ship!** ? This is a complete, production-ready app for real-world ADK agent interactions.