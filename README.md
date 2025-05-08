# LLM API Lab

A simple educational showcase project demonstrating local LLM inference via Ollama. 
This "agent")) extracts text from images, analyzes it, searches the web for relevant information, 
and summarizes the results using a few local LLMs via Ollama.

## Features

- Image text extraction with LLaVA
- Search query refinement with hyperparameter customized Phi-3 Mini
- Web search via DuckDuckGo
- Result summarization via Phi-3 Mini

## Running the Application

You can run this application either in local env or using Docker.

### Option 1: Running Locally

#### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com) installed locally
- Required models: `llava` (image-to-text) and `phi3:mini` (analysis)

#### Installation

1. Clone this repository
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Ollama models:
```bash
./setup.sh
```

5. Run the application:
```bash
python agent.py
```

6. Open the displayed URL in your browser (http://localhost:7860)
7. Upload an image with text to get results

### Option 2: Running with Docker

#### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### Setup and Run

1. Clone this repository
2. Start the services:
```bash
docker-compose up -d
```

This will:
- Pull the Ollama image
- Build the agent container
- Initialize required models (llava, phi3:mini, and custom search-query-generator)
- Start all services

4. Access the application at:
```
http://localhost:7860
```

## Docker Architecture

The Docker setup consists of:
- **Ollama container**: Provides LLM inference services
- **Init-ollama container**: Sets up required models
- **Agent container**: Runs the Python application

## Customization

### Environment Variables

- `OLLAMA_HOST`: The hostname of the Ollama service (default: "ollama" in Docker, "localhost" for local setup)
- `OLLAMA_PORT`: The port of the Ollama service (default: 11434)

### Models

- `llava`: For image vision capabilities
- `phi3:mini`: For generating summaries
- `search-query-generator`: Custom model created from the Modelfile

## License

MIT License - See the [LICENSE](LICENSE) file for details.

## Author

Bohdan Lukashchuk
