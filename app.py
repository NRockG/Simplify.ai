import gradio as gr
import google.generativeai as genai
import os

# Set your Google AI Studio API Key
API_KEY = os.getenv("GEMINI_API_KEY")  # Retrieve key securely

if not API_KEY:
    raise ValueError("Error: GEMINI_API_KEY is not set. Please add it as an environment variable.")


genai.configure(api_key=API_KEY)

# Define the generation configuration for the model
generation_config = {
    "max_output_tokens": 512,  # You can adjust this value
    "temperature": 0.7,        # Adjust temperature for randomness
    "top_p": 0.95              # Adjust top_p for sampling control
}

# Load the Gemini model
model = genai.GenerativeModel(model_name="gemini-2.0-flash", generation_config=generation_config)

# System instructions for the chatbot
SYSTEM_INSTRUCTIONS = """
Your name is *Simplify*, a helpful AI assistant designed to interpret and simplify complex information. 
Users will provide you with text or image data. Your task is to:
1. **Understand:** Thoroughly analyze the input text or image to identify its core meaning, key concepts, and underlying context.
2. **Simplify:** Re-express the information in a clear, concise, and easily understandable manner. Tailor the simplification to be appropriate for a general audience with no specialized knowledge.
3. **Explain:** Provide the simplified explanation in a conversational, chatbot-like format.
When responding, consider that the user may have limited background knowledge. Ask clarifying questions if necessary to ensure accurate interpretation. Also, introduce yourself with a smiley face emoji 😃.
"""

# Chatbot function
def respond(message, history, system_message, max_tokens, temperature, top_p):
    # Combine system instructions with the first user message
    if not history:
        chat_history = [{"role": "user", "parts": [SYSTEM_INSTRUCTIONS]}]  # Add system instructions as first message
    else:
        chat_history = []

    # Add previous chat history
    for user, bot in history:
        if user:
            chat_history.append({"role": "user", "parts": [user]})
        if bot:
            chat_history.append({"role": "assistant", "parts": [bot]})

    # Add the new user message
    chat_history.append({"role": "user", "parts": [message]})

    # Debugging: Log the full chat history
    print(chat_history)

    # Generate response
    response = model.generate_content(
        chat_history,
        generation_config={
            "max_output_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    )

    return response.text


# Create Gradio chatbot UI
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="Simplify AI - Ready to help! 😃", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
)

if __name__ == "__main__":
    demo.launch()
