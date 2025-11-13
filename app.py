from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline
import io
from PIL import Image
import base64

app = Flask(__name__)
CORS(app)

def get_dimensions(ratio_str):
    base_size = 512
    
    parts = ratio_str.split(':')
    if len(parts) != 2:
        return base_size, base_size 

    try:
        w_ratio = int(parts[0])
        h_ratio = int(parts[1])
    except ValueError:
        return base_size, base_size

    max_dim = 768 

    if w_ratio > h_ratio:
        width = max_dim
        height = int(max_dim * h_ratio / w_ratio)
    elif h_ratio > w_ratio:
        height = max_dim
        width = int(max_dim * w_ratio / h_ratio)
    else:
        width = base_size
        height = base_size
        
    width = (width // 8) * 8
    height = (height // 8) * 8
    

    if width > 768 or height > 768:
        width = min(width, 768)
        height = min(height, 768)
        
    
    if width < 512 and height < 512:
         
        if width < height:
            width = 512
            height = int(512 * h_ratio / w_ratio)
        else:
            height = 512
            width = int(512 * w_ratio / h_ratio)
        
        
        width = (width // 8) * 8
        height = (height // 8) * 8


   
    width = max(512, min(width, 768))
    height = max(512, min(height, 768))

    return width, height



print("Loading Stable Diffusion model...")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


dtype = torch.float16 if device == "cuda" else torch.float32 

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=dtype
)
pipe = pipe.to(device)
print("Model loaded successfully.")



@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        ratio = data.get("ratio", "1:1") 

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

      
        width, height = get_dimensions(ratio)
        
        print(f"Generating image for prompt: '{prompt}' with size {width}x{height} (Ratio: {ratio})")

        result = pipe(
            prompt,
            width=width,         
            height=height,       
            num_inference_steps=30,
            guidance_scale=7.5
        )

        image = result.images[0]

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({"image": img_str})

    except torch.cuda.OutOfMemoryError:
       
        print("CUDA Out of Memory Error occurred. Please try 1:1 ratio.")
        return jsonify({"error": "System out of memory (OOM). Please use the 1:1 (Square) aspect ratio, which is safer for 4GB VRAM."}), 500
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)