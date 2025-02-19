# ChatGPT-Godmode

ChatGPT-Godmode is a Python application that leverages the OpenAI GPT API to generate, execute, and iteratively fix Python code based on user instructions. With a modern, ChatGPT-inspired interface built using Tkinter, this tool enables you to interactively command the AI to create or improve programs in real time. All generated code is also saved in a persistent directory for later review.

## ⚠️ Warning:
Dynamically generated code can be dangerous. Use this tool only in a secure, controlled environment and review the generated code before execution.

---

## 📌 Overview
ChatGPT-Godmode employs a meta-programming approach where GPT acts as the “brain” to:

- **Generate Code:** Produce complete, executable Python programs from your prompts.
- **Execute Code:** Run the generated code and capture its output.
- **Iterative Debugging:** Automatically detect errors and refine the code until it runs successfully (or until a maximum number of iterations is reached).
- **Persistent Storage:** Save every generated code file in the `generated_programs` folder with a timestamped filename.

---

## ✨ Features
- **ChatGPT-like UI:** Scrollable, modern chat interface with distinct chat bubbles for User, Assistant, and System messages.
- **Dynamic Code Generation:** Leverages the OpenAI GPT API (with a configurable model) to generate complete Python code based on user input.
- **Automated Debugging:** Iteratively refines code by sending error details back to GPT until the code runs without issues.
- **Persistent Code Storage:** Automatically saves all generated code files in the `generated_programs` directory for future reference.
- **Customizable Model:** Easily switch between models (like `gpt-4` or `gpt-3.5-turbo`) by modifying a single variable in the code.

---

## 🛠️ Prerequisites
- **Python 3.7 or later**
- **Tkinter:** Usually bundled with Python (if not, install it via your package manager).
- **OpenAI Python Package:** Install via pip:
  ```bash
  pip install openai
  ```
- **OpenAI API Key:** Obtain an API key from OpenAI.

---

## 📥 Installation
### Clone the Repository:
```bash
git clone https://github.com/yourusername/ChatGPT-Godmode.git
cd ChatGPT-Godmode
```

### Install Required Packages:
```bash
pip install -r requirements.txt
```
If no `requirements.txt` is provided, ensure that you have the OpenAI package installed.

### Configure Your API Key and Model:
Open the main Python file (e.g., `main.py`) and replace `"YOUR_API_KEY"` with your actual OpenAI API key. To change the model, update the `OPENAI_MODEL` variable at the top of the file:
```python
OPENAI_MODEL = "gpt-4"  # Change to "gpt-3.5-turbo" or another supported model if needed.
```

---

## 🚀 Running the Application
Start ChatGPT-Godmode by running:
```bash
python main.py
```
A Tkinter window will open displaying a ChatGPT-like chat interface. Type your prompt (e.g., *"Create a basic calculator program"*) and press **Enter** or click the **Send** button. The program will generate Python code, execute it, and display the outputs and any error messages. If errors occur, the tool will iteratively refine the code until it executes correctly or until the maximum number of iterations is reached.

---

## 💡 Usage Example
```
User: "Create a basic GUI calculator"
Assistant: Displays the generated Python code in a chat bubble.
System: Shows the saved file path, execution output, and error messages.
Assistant/System: Iteratively refines and updates the code until a final, error-free version is achieved.
```

---

## ⚠️ Disclaimer
### Security Notice:
Executing dynamically generated code poses risks. Use ChatGPT-Godmode only in a secure, isolated environment and always review the code before running it.

### Experimental:
This project is experimental and intended for educational and demonstration purposes. Use it at your own risk.

---

## 🤝 Contributing
Contributions, bug reports, and feature suggestions are welcome! Please open an issue or submit a pull request.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements
- **OpenAI:** For providing the GPT API that powers this tool.
- **ChatGPT:** Inspiration behind the modern, interactive chat interface.
- **Community:** Thanks to all contributors and the community for ongoing support and inspiration.
