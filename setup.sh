#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Setting up Ollama models for AI Vision Assistant...${NC}"

export OLLAMA_SKIP_CUDA=1

export OLLAMA_PORT=11434
echo -e "${GREEN}Using Ollama port: ${OLLAMA_PORT}${NC}"

echo -e "${GREEN}Running in CPU-only mode (CUDA disabled)${NC}"

if ! command -v ollama &> /dev/null; then
    echo -e "${RED}Ollama is not installed. Please install it from https://ollama.com${NC}"
    exit 1
fi

if ! curl -s http://localhost:11434/api/version &> /dev/null; then
    echo -e "${YELLOW}Starting Ollama service...${NC}"
    ollama serve &> /dev/null &

    for i in {1..10}; do
        if curl -s http://localhost:11434/api/version &> /dev/null; then
            echo -e "${GREEN}Ollama service started successfully${NC}"
            break
        fi
        if [ $i -eq 10 ]; then
            echo -e "${RED}Failed to start Ollama service${NC}"
            exit 1
        fi
        sleep 1
    done
else
    echo -e "${GREEN}Ollama service is already running${NC}"
fi

echo -e "${YELLOW}Initializing Ollama models...${NC}"

export OLLAMA_HOST=${OLLAMA_HOST:-localhost}
echo -e "${GREEN}Using OLLAMA_HOST=${OLLAMA_HOST}${NC}"

if bash ./init-ollama.sh; then
    echo -e "${GREEN}Successfully initialized Ollama models${NC}"
else
    echo -e "${RED}Failed to initialize Ollama models${NC}"
    exit 1
fi

echo -e "\n${GREEN}All models are ready. You can now run the agent with: python agent.py${NC}"
