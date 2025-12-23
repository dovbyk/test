import re
import os
import uuid
import subprocess
import shutil

def clean_llm_code_file(filepath):

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    code = re.sub(r'^\s*```(?:python)?\s*\n', '', code, flags=re.IGNORECASE | re.MULTILINE)
    code = re.sub(r'\s*```\s*$', '', code, flags=re.MULTILINE)

    code = code.replace('`', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code.strip() + '\n')

    print("Clean completed from inside the function")




def extract_class_name(script_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    match = re.search(r'class\s+(\w+)\s*\(\s*VoiceoverScene\s*\)\s*:', script_text)
    if match:
        return match.group(1)
    raise ValueError("No VoiceoverScene class found in script.")

def save_script(script_text, directory):
    script_id = str(uuid.uuid4())
    script_path = os.path.join(directory, f"{script_id}.py")
    with open(script_path, "w") as f:
        f.write(script_text)

    print("Saved the script")
    return script_path, script_id

def render_manim(script_path, output_dir, class_name):
    print("Starting calling render_manim")
    print(f"Class name extracted is {class_name}")
    
    manim_path = shutil.which("manim")
    if not manim_path:
        raise RuntimeError("Manim executable not found in PATH")

    print(f"Going to run command and look at manim path {manim_path}")
    cmd = [
        manim_path,
        "-pql",
        script_path,
        class_name,
        "--media_dir", output_dir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("LLM generated code had error")

        # Extract only the traceback portion
        stderr = result.stderr
        traceback_index = stderr.find("Traceback")
        short_error = stderr[traceback_index:] if traceback_index != -1 else stderr

        raise RuntimeError(short_error.strip())

    video_path = os.path.join(
        output_dir, "videos",
        os.path.splitext(os.path.basename(script_path))[0],
        "480p15",
        f"{class_name}.mp4"
    )

    print(f"Printing the current video path {video_path}")
    if not os.path.exists(video_path):
        raise FileNotFoundError("Rendered video not found.")

    print("Sending video path from render manim function")
    return video_path
