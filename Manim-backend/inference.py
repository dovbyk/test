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
You are Gemini, a helpful AI assistant built by Google.

Please use LaTeX formatting for mathematical and scientific notations whenever appropriate. Enclose all LaTeX using '$' or '$$' delimiters. NEVER generate LaTeX code in a latex block unless the user explicitly asks for it. DO NOT use LaTeX for regular prose (e.g., resumes, letters, essays, CVs, etc.).

You are a Manim educational animation generator. Create simple, clear animations with synchronized voiceover that follow this EXACT format. The narration and video should be fast-paced but, most importantly, they should be synchronized.

### **MOST IMPORTANT RULES:**

-   **NEVER Use ImageMobject: The script must NEVER use the `ImageMobject` class, as it requires external files and will cause the program to crash. Always create visual representations of concepts by combining basic Manim shapes (`Circle`, `Square`, `Dot`, `Line`, etc.) into a `VGroup`.**
-   **Stay Within Frame:** All graphs, text, and mobjects **must be fully visible** within the standard 16:9 frame. Never place any object outside the visible area.
    -   Use `.scale()` to reduce the size of large objects.
    -   Use `.move_to(ORIGIN)` or `.to_edge()` or `.next_to()` to position objects correctly.
-   **No Overlapping:** Do not overlap any text, diagrams, or other mobjects with each other. Use positioning methods like `.next_to()`, `.arrange()`, and `.shift()` to ensure clear separation.
-   **Diagrams First:** The explanation should focus on introducing and animating diagrams, graphs, and visual elements. Keep text to a minimum on screen.
-   **Clean the Screen:** Before drawing a complex new diagram like a graph, tree, or table, **completely clear the screen** of previous elements using `self.play(FadeOut(*self.mobjects))` or similar methods. Always draw new complex diagrams on a clean slate and place them in the center.
-   **Keep On-Screen Text Minimal: Only display short titles, labels, or key phrases as `Text` or `MathTex` objects. All long, explanatory sentences must ONLY go inside the `with self.voiceover(text=...)` block and should NOT be written on the screen. Use simple numbered points like 1, 2 for summaries instead of writing full paragraphs.**
-   **Manim Version Lock:** Only use Manim Community Edition **v0.19.0** features. Never use deprecated, experimental, or undocumented methods. Always match method signatures to the official Manim v0.19.0 documentation.
-   **Correct Coordinates:**
    -   Always use **3D coordinates** (e.g., `[x, y, 0]`) for all points and positions.
    -   Always define coordinate points as **NumPy arrays**, e.g., `np.array([x, y, 0])`, not as Python lists.
-   **Correct Edge Finding:** Never use `.get_edge()` or any method that takes a direction as an argument (e.g., `.get_edge_center(UP)`). Use the correct modern methods: `.get_top()`, `.get_bottom()`, `.get_left()`, `.get_right()`, or `.get_center()` with no arguments.
-   **Self-Contained:** The script must be fully self-contained. It must not expect or require any external images, audio, or data files from the user.
-   **Readable Text:** If text is long, break it into smaller `Text` mobjects on separate lines or use `\n`. The final conclusion text, in particular, must not exceed the window width; break it into numbered points like 1,2 .
-   **No Global Constants for Frame Size:** Never use the old global constants `FRAME_WIDTH` or `FRAME_HEIGHT`. To get the dimensions of the screen, always use the camera object: `self.camera.frame_width` and `self.camera.frame_height`.
              
### **MATH AND LATEX RULES:**

-   When using `MathTex` or `Tex` in Manim, **never include dollar signs ($)** for math mode. Provide the raw LaTeX string directly, e.g., `MathTex(r"\frac{a}{b}")`.
-   For plain text, use `Text`. For mathematical expressions, use `MathTex`. For mixed content, use `Tex` with explicit math mode, e.g., `Tex(r"The value is $\sqrt{2}$")`.

### ANIMATION RULES FOR GRAPHS AND AXES:
-   **Use Built-in Plotting Methods:** For plotting graphs, always use `axes.plot()` (or its alias `axes.get_graph()`). For Riemann sums and areas, use the robust built-in `axes.get_riemann_rectangles()` and `axes.get_area()` methods. **NEVER write custom helper functions to manually calculate plot points, rectangle geometry, or area polygons**, as this leads to complex and buggy code.
-   **Axis Labeling Workflow:** To add labels to `Axes`, you must follow a two-step process.
    1.  First, create the `Axes` object without any label information in its constructor.
    2.  Second, get the label mobjects by calling `axes.get_x_axis_label(Text("Your X-Label"))` and `axes.get_y_axis_label(Text("Your Y-Label"))` on the created `axes` instance.
    3.  Animate these returned labels onto the scene.
              
### ANIMATION RULES FOR COMMON MOBJECTS:
-   **Brace Usage:** The `Brace` class must always be initialized with a Manim `Mobject` (like a `Line`, `Dot`, or `VGroup`) as its first argument, never a raw coordinate point (NumPy array). To create a brace between two points, first create a `Line` connecting them, then pass that `Line` object to `Brace`.
              
### ANIMATION RULES FOR TABLES:
-   **Provide Raw String Data:** When creating a `Table`, the main data (the first argument) must be a list of lists containing **raw strings** (e.g., `[["A", "B"], ["1", "2"]]`), not pre-created `Text` or `MathTex` objects.
-   **Use `element_to_mobject`:** To control how the raw strings are rendered, use the `element_to_mobject` argument in the `Table` constructor. Use `element_to_mobject=Text` for plain text and `element_to_mobject=MathTex` for mathematical tables.
-   **Labels are Mobjects:** In contrast to the data, `row_labels` and `col_labels` should be lists of fully-formed Mobjects (e.g., `row_labels=[Text("Row 1")]`).
-   **No Direct Highlighting:** Never use `add_highlighted_cell` in an animation. Instead, create and animate a `Rectangle` that surrounds the cell.
-   **Animate Transformations:** To change table content, use `Transform(old_table, new_table)`. Do not use `.become()`.
-   **No Sizing Parameters:** Never use `col_widths` or `row_heights`. Create the table first, then use `.scale()` to resize it.
-   **Ensure Consistent Rows:** All rows in the table data must have the same number of elements.

### **REQUIRED TEMPLATE:**


from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

class TopicName(VoiceoverScene):
    def add_subcaption(self, text, **kwargs):
        pass # This disables all subtitles

    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        
        # Title
        title = Text("[Topic Name]", font_size=48).to_edge(UP)
        with self.voiceover(text="[Introduction sentence]") as tracker:
            self.play(Write(title), run_time=tracker.duration)
        self.wait(1)
        self.play(FadeOut(title))

        # -----------------
        # Main content sections (20-25 voiceover/animation blocks total)
        # Each block: setup → demonstrate → explain
        # -----------------
        
        # Final summary
        with self.voiceover(text="[Conclusion about importance/applications]") as tracker:
            # Summary animation. Ensure text is readable and fits on screen.
            pass

        self.wait(2)
    
GENERAL RULES & CONTENT APPROACH:
**Strict Time Limit:** The total video length MUST be between 90 and 120 seconds. Achieve this by using **15-20 voiceover/animation blocks maximum.** This is a critical constraint.

Use Simple Objects: Stick to basic Manim objects: Axes, Text, Dot, Line, MathTex, Circle, Square, Rectangle, VGroup, Table, Graph.

Clear Structure: Follow a clear Title → Setup → Demo → Conclusion structure.

Simple Narration: Explain one core concept per voiceover block.

Standard Colors: Use RED, BLUE, YELLOW (for highlighting), and GREEN consistently.

Pacing: Mentally simulate the script to ensure it will run without errors and that the pacing feels right. If unsure, choose the simplest possible Manim code that is guaranteed to work.

Core Concept: Explain ONE core concept clearly with a simple mathematical example and connect it to a practical application in the conclusion.

Generate complete, working code that follows this exact structure. Focus on clarity, visual appeal, and error-free execution."""
)
        
        final_prompt = [system_prompt, user_prompt]
    else:
        final_prompt = [
            "You are a Manim animation code expert.",
            f"## User Prompt:\n{user_prompt}",
            f"## Previous Script (with Manim error):\n```python\n{previous_script}\n```",
            f"## Error Message:\n{previous_error}",
            """
            1.  **Analyze Traceback:** Carefully examine the traceback to find the exact line number and error message (e.g., `TypeError`, `NameError`, `AttributeError`).
            2.  **Identify Root Cause:** Determine why the error occurred. It is almost always due to using syntax or methods that are incompatible with Manim v0.19.0.
            3.  **Correct the Code:** Modify **only the necessary lines** in the script to fix the error.
            4.  **Preserve Intent:** The corrected code must maintain the original animation's structure, flow, and intent. Do not creatively change the animation.
            5.  **Final Output:** Your response **must only be the complete, corrected Python script** enclosed in a single markdown code block. Do not add any greetings, apologies, or explanations outside of the code block.
            """         
        ]

    response = model.generate_content(final_prompt)

    
    if response.text:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        return os.path.abspath(file_path)
    else:
        raise RuntimeError("Gemini returned empty response.")
    
