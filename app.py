import streamlit as st
import requests
import datetime
import os
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("STABILITY_API_KEY")

def generate_image(prompt, model, mode, aspect_ratio, output_format, negative_prompt=None, seed=0, style_preset=None, image_path=None, strength=None):
    if model == "stable-core":
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    else:
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/*"
    }
    files = {
        "prompt": (None, prompt),
        "output_format": (None, output_format),
        "seed": (None, str(seed))
    }
    if negative_prompt:
        files["negative_prompt"] = (None, negative_prompt)

    if model.startswith("sd3"):
        files["model"] = (None, model)
        files["mode"] = (None, mode)
        if mode == 'text-to-image':
            files["aspect_ratio"] = (None, aspect_ratio)
        elif mode == 'image-to-image':
            if image_path:
                # Ensure the image is read as binary
                files['image'] = (image_path.name, image_path.getvalue(), 'image/png')
            if strength is not None:
                files['strength'] = (None, str(strength))
    else:
        files["aspect_ratio"] = (None, aspect_ratio)
        if style_preset:
            files["style_preset"] = (None, style_preset)

    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 403:
            error_message = response.json().get("name")
            if error_message == "content_moderation":
                return {"error": "content_moderation"}
            else:
                return {"error": error_message}
        else:
            response.raise_for_status()
            return response
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to make request: {e}")
        return None

def main():
    st.title("StabilityAI API Playground ⚡️")
    api_choice = st.selectbox("Select API:", ["Stable Core", "Stable Diffusion 3.0"])
    
    if api_choice == "Stable Diffusion 3.0":
        models = ['sd3']
        use_sd3_turbo = st.checkbox("Enable SD3 Turbo", value=False)
        if use_sd3_turbo:
            models.append('sd3-turbo')
    else:
        models = ['stable-core']

    prompt = st.text_input("Enter your prompt:")
    mode = 'text-to-image'
    image_file = None
    strength = None

    if api_choice == "Stable Diffusion 3.0":
        mode = st.selectbox("Select the mode:", ["text-to-image", "image-to-image"])
        if mode == 'image-to-image':
            image_file = st.file_uploader("Upload your image:", type=['png', 'jpg', 'jpeg'])
            strength = st.slider("Select strength (0.0 to 1.0):", 0.0, 1.0, 0.5)

    aspect_ratio = st.selectbox("Select aspect ratio:", ["1:1", "16:9", "3:2", "5:4", "4:5", "2:3", "9:16", "9:21"])
    output_format = st.selectbox("Select output format:", ["png", "jpeg", "webp"])
    negative_prompt = st.text_input("Enter negative prompt (optional):")
    seed = st.number_input("Enter seed (optional, 0 for random):", value=0, min_value=0, max_value=4294967294, step=1)

    style_preset = None
    if api_choice == "Stable Core":
        style_preset = st.selectbox("Select style preset (optional):", ["", "enhance", "anime", "photographic", "digital-art", "comic-book", "fantasy-art", "line-art", "analog-film", "neon-punk", "isometric", "low-poly", "origami", "modeling-compound", "cinematic", "3d-model", "pixel-art", "tile-texture"])

    if st.button("Generate Image"):
        if not prompt:
            st.error("Please enter a prompt.")
        else:
            with st.spinner("Generating images..."):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(generate_image, prompt, model, mode, aspect_ratio, output_format, negative_prompt, seed, style_preset, image_file, strength) for model in models]
                    results = [future.result() for future in futures]

            output_folder = './outputs'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for result, model in zip(results, models):
                if result is not None:
                    if "error" in result:
                        if result["error"] == "content_moderation":
                            st.error("Your request was flagged by the content moderation system. Please modify your prompt and try again.")
                        else:
                            st.error(f"Error generating image with {model}: {result['error']}")
                    else:
                        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S").lower()
                        model_prefix = model.replace("-", "_")
                        output_image_path = f"{output_folder}/{model_prefix}_output_{current_time}.{output_format}"
                        with open(output_image_path, 'wb') as file:
                            file.write(result.content)
                        st.image(output_image_path, caption=f"Generated with {model}")
                else:
                    st.error(f"Failed to generate with {model}")

if __name__ == "__main__":
    main()
