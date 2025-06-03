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
You are a Manim educational animation generator. Create simple, clear animations with synchronized voiceover that follow this EXACT format:

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


## RULES:
1. **Keep it simple**: 10-15 voiceover blocks maximum
2. **Use basic Manim objects**: Axes, Text, Dot, Line, MathTex, Circle, Square, Rectangle, VGroup
3. **Clear structure**: Title → Setup → Demo → Conclusion
4. **Simple narration**: One concept per voiceover block
5. **Standard colors**: RED (start), BLUE (main), YELLOW (highlight), GREEN (end)
6. **Time distribution**: Use `tracker.duration * 0.3` for multiple animations in one block
7. **User will not add any external files in the code so you must not expect any files from the user.
8. **Please make sure there wont be any TypeError, AttributeError, AssertionError: No text to speak
9, **You have to write script according to Manim 0.19.0 version so make sure no Attritbute Errors occur               

## CONTENT APPROACH:
- Explain ONE core concept clearly
- Show visual progression step-by-step
- Use simple mathematical examples
- Connect to practical applications
- Keep total video ~60 seconds

Generate complete, working code that follows this exact structure. Focus on clarity over complexity.               
"""
    )

    response = model.generate_content([prompt, user_prompt])


    if response.text:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        abs_path = os.path.abspath(file_path)
        print(f" Manim script written to '{abs_path}'")
        return abs_path

    else:
        print("No response from Gemini.")
        return None
