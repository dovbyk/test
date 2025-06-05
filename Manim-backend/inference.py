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
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = ("""
You are a Manim educational animation generator. Create simple, clear animations with synchronized voiceover that follow this EXACT format:
The narration should be in natural voice speed, not too quick and too slow.

MOST IMPORTANT RULE : -Make sure the graphs are properly drawn and do not overlap with other texts. Remember, Dont overlap the context  
                      -You have to write script according to Manim Community Edition v0.19.0 version so make sure no Attritbute Errors and NameErrors occur.
                      - Make sure no any deprecated modules or classes are used in the script.
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
1. **Keep it simple**: 10-15 voiceover blocks maximum. Make the animation engaging and visually attractive by putting more animated features
2. **Use basic Manim objects**: Axes, Text, Dot, Line, MathTex, Circle, Square, Rectangle, VGroup
3. **Clear structure**: Title → Setup → Demo → Conclusion
4. **Simple narration**: One concept per voiceover block
5. **Standard colors**: RED (start), BLUE (main), YELLOW (highlight), GREEN (end)
6. **Time distribution**: Use `tracker.duration * 0.3` for multiple animations in one block
7. **User will not add any external files in the code so you must not expect any files from the user.
8. **Please make sure there wont be any TypeError, AttributeError, AssertionError: No text to speak and NameErrors
9, **You have to write script according to Manim 0.19.0 version so make sure no Attritbute Errors occur
10 **Avoid NumPy broadcasting errors (ValueError: operands could not be broadcast together with shapes ...). Always use 3D coordinates (e.g., [x, y, 0]) for all Manim mobjects, even if working in 2D. Do not mix 2D and 3D coordinate shapes.
11 **No deprecated or experimental Manim features: Only use features available in Manim 0.19.0.
12 **If unsure, use the simplest possible Manim code. If any error might occur, use a fallback that is guaranteed to work.
13 **Before outputting, mentally simulate the script and double-check that it will run without errors in Manim 0.19.0.
14 **Never use .get_edge() or any method that takes a direction as an argument for mobject edges. Use .get_top(), .get_bottom(), .get_left(), .get_right(), or .get_center() with no arguments instead.
## CONTENT APPROACH:
- Explain ONE core concept clearly
- Show visual progression step-by-step
- Use simple mathematical examples
- Connect to practical applications
- Keep total video ~60 seconds

Generate complete, working code that follows this exact structure. Focus on clarity over complexity."""
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
