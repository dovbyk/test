from flask import Flask, request, send_file, jsonify
import os
from manim_utils import extract_class_name, save_script, render_manim, clean_llm_code_file
from inference import generate_manim_script

app = Flask(__name__)
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
    
    clean_llm_code_file(script_path)
    
    # 2. Extract class name
    #try:
    #    class_name = extract_class_name(script_text)
    #except Exception as e:
     #   return jsonify({"error": str(e)}), 400

    # 3. Save script
    # script_path, script_id = save_script(script_text, TEMP_DIR)

    # 4. Render video
    try:
        video_path = render_manim(script_path, TEMP_DIR)
    except Exception as e:
        return jsonify({"error": f"Render failed: {e}"}), 500

    # 5. Serve video
    return send_file(video_path, mimetype="video/mp4", as_attachment=True, download_name="Shit.mp4")
