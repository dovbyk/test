from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import time
from manim_utils import extract_class_name, save_script, render_manim, clean_llm_code_file
from inference import generate_manim_script

app = Flask(__name__)
CORS(
    app,
    origins="https://promptanimate.vercel.app", 
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"]
)

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.route('/wake-up', methods=['GET'])
def start_server():
    time.sleep(15)
    return jsonify({'msg': 'ok'}), 200
    


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # 1. Get Manim script from LLM
    MAX_RETRIES = 6
    attempt = 0
    error_msg = None
    current_script = None

    while attempt < MAX_RETRIES:
        script_path = None  # Initialize here to prevent UnboundLocalError
        try:
            attempt += 1  
            print(f"[Attempt {attempt}] Trying to generate Manim Script... ")
            script_path = generate_manim_script(prompt, current_script, error_msg)
            print("LLM Generated Manim Script file")
            clean_llm_code_file(script_path)
            class_name = extract_class_name(script_path)
            video_path = render_manim(script_path, TEMP_DIR, class_name)

            
            return send_file(video_path, mimetype="video/mp4", as_attachment=True, download_name="render.mp4")
        except Exception as e:
            error_msg = str(e)

            if script_path and os.path.exists(script_path):
                with open(script_path, "r") as f:
                    current_script = f.read()

            
            print(f"[Attempt {attempt}] Render failed. Retrying...\nError: {error_msg}\n")
    
    return jsonify({
        "error": f"All {MAX_RETRIES} attempts failed.",
        "last_error": error_msg
    }), 500


if __name__ == "__main__":
    # debug=True allows you to see errors and auto-restarts the server on code changes
    # port=5000 matches your Dockerfile and usual local testing defaults
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
