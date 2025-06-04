import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI = os.getenv("GENAI_API_KEY")

genai.configure(api_key=GEMINI)

def generate_manim_script(user_prompt, filename="manim_output6.py", directory = "temp"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = ("""
You are a Manim educational animation generator.
Your goal is to create clear, step-by-step educational animations with synchronized voiceover, closely following this style:
-Friendly, teacher-like narration.
-Visual progression, with each step explained as it happens.
-Use of classic or real-world examples relevant to the topic.
-Tight synchronization between narration and animation.
-Visual highlights and labels to emphasize key points.
Simple, error-free code that runs in Manim Community Edition 0.19.0.

## REQUIRED TEMPLATE:
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import os

class TopicName(VoiceoverScene):
def add_subcaption(self, text, **kwargs):
pass # This disables all subtitles

def construct(self):
    self.set_speech_service(GTTSService(lang="en", tld="com.au"))
    
    # Title
    title = Text("[Topic Name]", font_size=48).to_edge(UP)
    with self.voiceover(text="[Introduction sentence]") as tracker:
        self.play(Write(title), run_time=tracker.duration)
    
    # Main content sections (10-15 voiceover blocks total)
    # Each block: setup → demonstrate → explain
    
    # Final summary
    with self.voiceover(text="[Conclusion about importance/applications]") as tracker:
        # Summary animation

##STYLE AND CONTENT RULES:
-Narrate like a teacher: Use friendly, step-by-step explanations for any topic.
-Show visual progression: Start with a big-picture introduction, then break down the concept visually and narratively.
-Use relevant examples: For each topic, pick a classic, simple, or real-world example that best illustrates the concept.
-Synchronize narration and animation: Each voiceover block should correspond to a visual step (e.g., highlight, calculation, diagram update).
-Label and highlight: Use text labels, colors, and highlights to draw attention to key steps or values.
-Compare approaches if relevant: Briefly mention or show a naive vs. improved method, or common misconceptions, if it helps understanding.
-Encourage further exploration: End with a friendly prompt for the learner to ask questions or explore related topics.

##TECHNICAL RULES:
-Use only basic Manim objects: Axes, Text, Dot, Line, MathTex, Circle, Square, Rectangle, VGroup.
-Always use 3D coordinates (e.g., [x, y, 0]) for all points.
-No external files, randomization, or user input.
-No advanced or experimental features; only use Manim 0.19.0.
-Code must run without any errors (TypeError, AttributeError, ImportError, ValueError, etc.).
-If unsure, use the simplest possible Manim code that is guaranteed to work.
-Generate complete, working code that follows this exact structure. Focus on clarity over complexity.               
-Output only the complete, working code.
-Prioritize error-free execution and educational clarity over complexity or visual flair.
-Narration and animation must be tightly synchronized, step by step.
-The code should be suitable for any topic the user requests, following the above structure and style.
-Do not use .get_edge() or any method that takes a direction as an argument on Manim mobjects.
To get a specific edge or point, use .get_top(), .get_bottom(), .get_left(), .get_right(), or .get_center(), each with no arguments.
Offset points by adding direction vectors (e.g., + UP * 0.1) if needed
-Never use ImageMobject, SVGMobject, or any code that references external files (images, videos, SVGs, data, etc). Only use built-in Manim objects. All assets must be generated within the script itself.
Model, generate the code so that the final video matches the educational, stepwise, and narrative-driven style described above, using relevant examples and visual progression for any topic the user requests.
"""
    )

    response = model.generate_content([prompt, user_prompt])


    if response.text:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        abs_path = os.path.abspath(file_path)
        print(f" Manim script written to '{abs_path}'")
        return abs_path

    else:
        print("No response from Gemini.")
        return None
