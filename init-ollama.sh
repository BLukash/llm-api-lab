#!/bin/bash

set -e

OLLAMA_HOST=${OLLAMA_HOST:-localhost}
echo "Initializing Ollama models... (Using host: $OLLAMA_HOST)"

export OLLAMA_SKIP_CUDA=1
echo "Running in CPU-only mode (CUDA disabled)"

echo "Waiting for Ollama service to be ready..."
until curl -s http://$OLLAMA_HOST:11434/api/version &> /dev/null; do
  echo "Ollama not available yet, waiting..."
  sleep 2
done
echo "Ollama is ready!"

echo "Pulling llava model..."
ollama pull llava

echo "Pulling phi3:mini model..."
ollama pull phi3:mini

echo "Creating search-query-generator model from Modelfile..."
ollama create search-query-generator -f Modelfile

echo "All models initialized successfully!"