from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import os
from manim_utils import extract_class_name, save_script, render_manim, clean_llm_code_file
from inference import generate_manim_script

app = Flask(__name__)
CORS(
    app,
    origins="https://promptanimate.vercel.app",  # Use string, not list
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"]
)

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # 1. Get Manim script from LLM
    script_path = generate_manim_script(prompt)
    print("Cleaning started")
    clean_llm_code_file(script_path)
    
     #2. Extract class name
    try:
        class_name = extract_class_name(script_path)
        print(f"Class name extracted and it is {class_name}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # 3. Save script
    # script_path, script_id = save_script(script_text, TEMP_DIR)

    # 4. Render video
    print("Clean completed..")
    try:
        video_path = render_manim(script_path, TEMP_DIR, class_name)
    except Exception as e:
        return jsonify({"error": f"Render failed: {e}"}), 500

    print("Sending Video File")
    # 5. Serve video
    return send_file(video_path, mimetype="video/mp4", as_attachment=True, download_name="Shit.mp4")
