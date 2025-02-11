const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    displayMessage(message, 'user');
    userInput.value = '';

    // Simulate a delay for the bot response
    setTimeout(async () => {
        await fetchBotResponse(message);
    }, 500);
}

async function fetchBotResponse(message) {
    // Replace 'YOUR-FASTAPI-ENDPOINT' with your actual FastAPI endpoint
    const response = await fetch('https://huggingface.co/gravity30-simplify-ai.hf.space/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
        displayMessage('Error: Could not fetch bot response', 'bot');
        return;
    }

    const data = await response.json();
    displayMessage(data.response, 'bot');
}

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    messageElement.textContent = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
}
