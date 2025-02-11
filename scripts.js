import { Client } from "@gradio/client";

const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    displayMessage(message, 'user');
    userInput.value = '';

    try {
        const client = await Client.connect("Gravity30/Simplify.ai");
        const result = await client.predict("/chat", {
            message: message,
            system_message: "Simplify AI - Ready to help! 😃",
            max_tokens: 100,
            temperature: 0.7,
            top_p: 0.9,
        });
        displayMessage(result.data[0], 'bot'); // Assuming data is at result.data[0]
    } catch (error) {
        console.error("Error fetching bot response:", error);
        displayMessage("Error: Could not fetch bot response", 'bot');
    }
}

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
}
