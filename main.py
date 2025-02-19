import tkinter as tk
import openai
import subprocess
import sys
import re
import threading
import os
import datetime

# Set your OpenAI API key here (or set the OPENAI_API_KEY environment variable)
openai.api_key = ""

# Easily change the OpenAI model by updating this variable:
# You can change this to "gpt-3.5-turbo" or any other supported model.
OPENAI_MODEL = ""


def extract_code(text):
    """
    Extracts code from a markdown-formatted string.
    If a code block is found (i.e. enclosed in triple backticks), the content is returned.
    Otherwise, the full text is returned.
    """
    code_blocks = re.findall(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return text.strip()


def save_code_to_file(code, suffix=".py"):
    """
    Saves the given code into a persistent file under the 'generated_programs' directory.
    Returns the filename.
    """
    directory = "generated_programs"
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"generated_{timestamp}{suffix}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    return filename


def run_code(code):
    """
    Saves the given code to a persistent file and executes it using the same Python interpreter.
    Returns a tuple (stdout, stderr, filename) containing the captured output, error messages,
    and the path to the saved file.
    """
    filename = save_code_to_file(code, suffix=".py")
    process = subprocess.run([sys.executable, filename],
                             capture_output=True, text=True)
    return process.stdout, process.stderr, filename


def generate_code(prompt, conversation_history):
    """
    Appends the prompt to the conversation history and calls the GPT API to generate a Python program.
    The function returns a tuple: (extracted code, updated conversation history)
    """
    conversation = conversation_history.copy()
    conversation.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=conversation
    )
    code_response = response.choices[0].message.content
    updated_conversation = conversation + \
        [{"role": "assistant", "content": code_response}]
    return extract_code(code_response), updated_conversation


def create_and_execute_program(user_prompt, update_chat_callback):
    """
    Generates a Python program based on the user_prompt and executes it.
    If errors occur during execution, it sends the error details back to GPT to request a corrected version.
    The update_chat_callback function is used to update the UI with messages.
    """
    conversation = [
        {"role": "system", "content": (
            "You are a Python code generator. When given a prompt, generate a complete, "
            "executable Python program that fulfills the requirements. Provide only the code "
            "inside a markdown formatted code block (using triple backticks)."
        )}
    ]

    update_chat_callback(
        "System", "Generating initial code based on your prompt...")
    try:
        code, conversation = generate_code(user_prompt, conversation)
    except Exception as e:
        update_chat_callback("System", f"Error generating code: {str(e)}")
        return

    update_chat_callback(
        "Assistant", f"Generated Code:\n```python\n{code}\n```")
    stdout, stderr, filename = run_code(code)
    update_chat_callback("System", f"Code saved to: {filename}")
    update_chat_callback(
        "System", f"Execution output:\n{stdout}\nErrors:\n{stderr}")

    iteration = 0
    while stderr.strip():
        iteration += 1
        update_chat_callback(
            "System", f"Attempting to fix errors (Iteration {iteration})...")
        fix_prompt = (
            f"The previous code produced the following error:\n{stderr}\n"
            "Please provide a corrected version of the code."
        )
        try:
            code, conversation = generate_code(fix_prompt, conversation)
        except Exception as e:
            update_chat_callback(
                "System", f"Error generating fixed code: {str(e)}")
            return
        update_chat_callback(
            "Assistant", f"Updated Code:\n```python\n{code}\n```")
        stdout, stderr, filename = run_code(code)
        update_chat_callback("System", f"Updated code saved to: {filename}")
        update_chat_callback(
            "System", f"Execution output:\n{stdout}\nErrors:\n{stderr}")
        if iteration > 5:
            update_chat_callback(
                "System", "Too many iterations. Aborting fix attempts.")
            break

    update_chat_callback("System", f"Final output:\n{stdout}")


class ChatGPTUI:
    """
    A ChatGPT-like UI built with Tkinter.
    Displays messages in a scrollable conversation area with chat bubbles.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT-Godmode")
        self.root.configure(bg="#F7F7F8")

        # Create a canvas for the chat area with a vertical scrollbar
        self.chat_canvas = tk.Canvas(root, bg="#F7F7F8", highlightthickness=0)
        self.chat_scrollbar = tk.Scrollbar(
            root, command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scrollbar.pack(side="right", fill="y")

        # A frame inside the canvas to hold the messages
        self.chat_frame = tk.Frame(self.chat_canvas, bg="#F7F7F8")
        self.chat_canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw")
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all"))
        )

        # Input frame at the bottom
        self.input_frame = tk.Frame(root, bg="#F7F7F8")
        self.input_frame.pack(side="bottom", fill="x")
        self.input_field = tk.Entry(
            self.input_frame, width=80, font=("Helvetica", 12))
        self.input_field.pack(side="left", padx=10,
                              pady=10, fill="x", expand=True)
        self.input_field.bind("<Return>", self.on_enter)
        self.send_button = tk.Button(
            self.input_frame, text="Send", command=self.on_enter, font=("Helvetica", 12))
        self.send_button.pack(side="right", padx=10, pady=10)

    def add_message(self, sender, message):
        """
        Creates a chat bubble for a message and adds it to the conversation area.
        """
        bubble_frame = tk.Frame(self.chat_frame, bg="#F7F7F8", pady=5)
        if sender == "User":
            bg_color = "#DCF8C6"  # Light green for user messages
            anchor = "e"
        elif sender == "System":
            bg_color = "#E8E8E8"  # Light grey for system messages
            anchor = "center"
        else:  # Assistant
            bg_color = "#FFFFFF"  # White for assistant messages
            anchor = "w"

        bubble = tk.Label(bubble_frame, text=message, bg=bg_color,
                          wraplength=500, justify="left", padx=10, pady=5,
                          font=("Helvetica", 12), bd=1, relief="solid")
        bubble.pack(side="top", anchor=anchor, padx=10)
        bubble_frame.pack(fill="x", anchor=anchor)

        # Auto-scroll to the bottom
        self.chat_canvas.yview_moveto(1.0)

    def update_chat(self, sender, message):
        self.add_message(sender, message)

    def on_enter(self, event=None):
        user_input = self.input_field.get().strip()
        if user_input:
            self.update_chat("User", user_input)
            self.input_field.delete(0, tk.END)
            threading.Thread(target=create_and_execute_program,
                             args=(user_input, self.update_chat), daemon=True).start()


def main():
    root = tk.Tk()
    app = ChatGPTUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
