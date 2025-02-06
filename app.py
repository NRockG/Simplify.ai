import gradio as gr
import google.generativeai as genai
import os

# Set your Google AI Studio API Key
os.environ["GOOGLE_API_KEY"] = AIzaSyDGTrfALfYRqf0haAzkxG1Mwz1zMicxbl8
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Chatbot function
def respond(message, history, system_message, max_tokens, temperature, top_p):
    chat_history = []
    
    for user, bot in history:
        if user:
            chat_history.append({"role": "user", "parts": [user]})
        if bot:
            chat_history.append({"role": "model", "parts": [bot]})

    chat_history.append({"role": "user", "parts": [message]})

    # Generate response from your custom Gemini AI agent
    response = agent.generate_content(
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
        gr.Textbox(value="Your name is *Simplify* a helpful AI assistant designed to interpret and simplify complex information.  Users will provide you with text or image data.  Your task is to:

1.  **Understand:**  Thoroughly analyze the input text or image to identify its core meaning, key concepts, and underlying context.
2.  **Simplify:** Re-express the information in a clear, concise, and easily understandable manner.  Tailor the simplification to be appropriate for a general audience with no specialized knowledge.
3.  **Explain:** Provide the simplified explanation in a conversational, chatbot-like format."

"When responding, consider the user may have limited background knowledge. Ask clarifying questions if necessary to ensure accurate interpretation. Also, introduce yourself with a smiley face emoji.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
)

if __name__ == "__main__":
    demo.launch()
