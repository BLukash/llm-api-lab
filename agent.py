import os
import requests
import base64
import gradio as gr
from io import BytesIO
from duckduckgo_search import DDGS
from PIL import Image


os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.environ.get("OLLAMA_PORT", "11434")

def image_to_base64(image, max_size=(1024, 1024)):
    """Convert image to base64 string with proper resizing"""
    image.thumbnail(max_size, resample=Image.LANCZOS)

    buffered = BytesIO()
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background

    image.save(buffered, format="JPEG", quality=100)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    print(f"Image resized to: {image.size}")
    print(f"Base64 image length: {len(img_str)}")

    return img_str

def query_ollama(model, prompt, image=None):
    """Query Ollama API with text and optional image"""
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    if image:
        print("Image found: ", image)
        data_uri = image_to_base64(image)
        payload["images"] = [data_uri]
        print(f"Sending request to Ollama with model: {model}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error querying Ollama: {str(e)}")
        print(f"Response content: {response.content if 'response' in locals() else 'No response'}")
        return f"Error: {str(e)}"

def search_duckduckgo(query, num_results=5):
    """Search DuckDuckGo and return top results"""
    results = []
    with DDGS(timeout=20) as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append({
                "title": r["title"],
                "href": r["href"],
                "body": r["body"]
            })
    return results

def process_image(image):
    if image is None:
        return "Please upload an image."
    
    print("Processing image...")

    llava_prompt = "What text do you see in this image? Just extract the text, no additional explanation."
    extracted_text = query_ollama("llava", llava_prompt, image)
    
    print("Extracted text:", extracted_text)
    
    assessment_prompt = extracted_text
    assessment = query_ollama("search-query-generator", assessment_prompt)

    print(f"Assessment complete: {assessment}")

    search_results = search_duckduckgo(assessment)

    print(f"Search results done: {search_results}")

    if search_results:
        result_text = "\n\n".join([f"Title: {r['title']}\nContent: {r['body']}" for r in search_results])
        summary_prompt = (
            "You are an intelligent agent that generates concise summaries of search results.\n\n"
            f"Task: Read the following search results related to \"{extracted_text}\" and provide a clear, concise summary of the key information.\n\n"
            "Search results:\n"
            f"{result_text}\n\n"
            "Output only the summary."
        )
        summary = query_ollama("phi3:mini", summary_prompt)
    else:
        summary = "No search results found."

    search_links = ""
    for r in search_results:
        search_links += f"- [{r['title']}]({r['href']})\n"

    response = (
        f"## Extracted Text\n"
        f"{extracted_text}\n\n"
        f"## Assessment\n"
        f"{assessment}\n\n"
        f"## Search Results\n"
        f"{search_links}\n"
        f"## Summary\n"
        f"{summary}"
    )

    return response

with gr.Blocks(title="AI Vision Assistant", analytics_enabled=False) as demo:
    gr.Markdown("# AI Vision Assistant")
    gr.Markdown("Upload an image to extract text, search the web, and get a summary of the information.")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload Image")
            submit_button = gr.Button("Process Image")
        
        with gr.Column():
            output_text = gr.Markdown()
    
    submit_button.click(
        fn=process_image,
        inputs=input_image,
        outputs=output_text
    )

if __name__ == "__main__":
    print("Starting the AI Vision Assistant...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
