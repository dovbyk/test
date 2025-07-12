import os


def generate_manim_script(user_prompt, previous_script=None, previous_error = None, filename="manim_output6.py", directory = "temp"):
    import google.generativeai as genai
    import random
    
    from dotenv import load_dotenv
    load_dotenv()
    keys = os.getenv("GEMINI_KEYS", "").split(",")
    genai.configure(api_key=random.choice(keys))

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    model = genai.GenerativeModel("gemini-2.0-flash")

    if not previous_script or not previous_error:
        system_prompt = ("""
You are a Manim educational animation generator. Create simple, clear animations with synchronized voiceover that follow this EXACT format:
The narration and video should be fast paced but most importantly they should be synchronized. Make sure to use small fonts so that texts or animation do not exceed the aspect ratio of 16:9

MOST IMPORTANT RULES:
- Keep the Manim script more diagrammatic rather than text-intensive.
- If you are explaining any algorithms and if you need to draw graph or tree for explaining topics like Heap Sort, Merge Sort, then consider drawing the graph after cleaning the entire screen. Keep them in the center of the screen. 
- If you are drawing a graph or tree or any table, then first clean the existing content and then draw. Make sure the diagrams are within the frame and they donot overlap with each other
- The explanation should focus more on introducing graphs, diagrams more so that the animation is visually attractive and intuitive.
- Don't overlap any texts or diagrams with each other 
- All graphs and mobjects must be fully visible within the standard 16:9 frame. Never place any object outside the visible area. Use .scale() and .move_to(ORIGIN) as needed to ensure everything fits and is centered. Do not overlap graphs with text or other mobjects.
- Only use Manim Community Edition v0.19.0 features. Never use deprecated, experimental, or undocumented methods or parameters. Always match method signatures to the Manim 0.19.0 documentation.
- Always use 3D coordinates (e.g., [x, y, 0]) for all points and positions, even for 2D scenes.
- Always define all coordinate points as NumPy arrays, e.g., np.array([x, y, 0]), not as Python lists. This ensures that any arithmetic (addition, division, averaging) on coordinates works correctly in Manim.
- Never use .get_edge() or any method that takes a direction as an argument for mobject edges. Use .get_top(), .get_bottom(), .get_left(), .get_right(), or .get_center() with no arguments instead.
- The script must be fully self-contained and must not expect or require any external files from the user.

## MATH AND LATEX RULES
- When using MathTex or Tex in Manim, never include dollar signs ($) for math mode. Always provide the LaTeX string directly, e.g., MathTex(r"\infty") not MathTex(r"$\infty$").
- Only use valid LaTeX commands for math symbols (e.g., \infty, \sqrt{2}, \frac{a}{b}) and do not nest math environments.
- For plain text, use Text. For mathematical expressions, use MathTex. For mixed text and math, use Tex with explicit math mode (e.g., Tex(r"Text with math: $\frac{1}{2}$")).

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
        
        # Main content sections (25-30 voiceover/animation blocks total)
        # Each block: setup → demonstrate → explain
        
        # Final summary
        with self.voiceover(text="[Conclusion about importance/applications]") as tracker:
            # Summary animation

## RULES:
1. Keep it simple: 25-30 voiceover/animation blocks maximum. Make the animation engaging and visually attractive by putting more animated features.
2. Use only basic Manim objects: Axes, Text, Dot, Line, MathTex, Circle, Square, Rectangle, VGroup.
3. Clear structure: Title → Setup → Demo → Conclusion.
4. Simple narration: One concept per voiceover block.
5. Standard colors: RED (start), BLUE (main), YELLOW (highlight), GREEN (end).
6. Time distribution: Use tracker.duration * 0.3 for multiple animations in one block.
7. Never expect or require any external files from the user.
8. Always use 3D coordinates for all mobject positions.
9. Never use deprecated, experimental, or undocumented Manim features; always check compatibility with Manim 0.19.0.
10. Mentally simulate the script and double-check that it will run without errors in Manim 0.19.0 before outputting.
11. Never use .get_edge() or any method that takes a direction as an argument for mobject edges. Use .get_top(), .get_bottom(), .get_left(), .get_right(), or .get_center() with no arguments instead.
12. Keep all content within the visible frame and avoid overlapping mobjects.
13. If unsure, use the simplest possible Manim code. If any error might occur, use a fallback that is guaranteed to work.
              
## ANIMATION RULES FOR TABLES AND HIGHLIGHTING
- **Never use `add_highlighted_cell` directly in animations**: 
  - Instead create temporary rectangles and animate their creation
  - Example of **WRONG**: `self.play(table.add_highlighted_cell(...))`
  - Example of **RIGHT**: 
    ```
    rect = Rectangle(color=YELLOW).surround(table.get_cell((1,1)))
    self.play(Create(rect))
    ```
- **Table modifications must use proper animations**:
  - Use `Transform(old_table, new_table)` instead of `table.become()`
  - Pre-create all table versions upfront rather than modifying during animation

- Never use `col_widths` or `row_heights` parameters with Manim's `Table` class
- Use `.scale()` to adjust table size instead
- Ensure all table rows have the same number of elements
              
## CONTENT APPROACH:
- Explain ONE core concept clearly.
- Show visual progression step-by-step.
- Use simple mathematical examples.
- Connect to practical applications.
- Keep total video at most or near about 120 seconds.

Generate complete, working code that follows this exact structure. Focus on clarity over complexity..""" 
)
        
        final_prompt = [system_prompt, user_prompt]
    else:
        final_prompt = [
            "You are a Manim animation code expert.",
            f"## User Prompt:\n{user_prompt}",
            f"## Previous Script (with Manim error):\n```python\n{previous_script}\n```",
            f"## Error Message:\n{previous_error}",
            "Please fix only the parts of the code that cause the error. Do not change the overall structure, naming conventions, voiceover blocks, or formatting.",
            "Avoid modifying parts of the code that are already valid. Only minimal necessary edits should be made.",
            "Only use the Manim 0.19.0 version compatible methods and classes."
            "Return corrected code only. No markdown formatting, no explanations."
        ]

    response = model.generate_content(final_prompt)

    
    if response.text:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        return os.path.abspath(file_path)
    else:
        raise RuntimeError("Gemini returned empty response.")
    
