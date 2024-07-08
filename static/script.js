let chatState = 'init';

function sendOption(option) {
    document.getElementById('userInput').value = option;
    sendMessage();
}

function sendMessage() {
    const inputField = document.getElementById('userInput');
    const message = inputField.value;
    const chatbox = document.getElementById('messages');
    const language = document.getElementById('languageSelect').value;

    if (message.trim() === '') return;

    // Add user message to chatbox
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.textContent = message;
    chatbox.appendChild(userMessage);

    // Clear input field
    inputField.value = '';

    // Scroll to the bottom
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send message to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message, state: chatState, language: language })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.url;
        } else {
            // Add bot response to chatbox
            const botMessage = document.createElement('div');
            botMessage.classList.add('bot-message');
            botMessage.innerHTML = data.response; // Use innerHTML to support HTML content
            chatbox.appendChild(botMessage);

            // Scroll to the bottom
            chatbox.scrollTop = chatbox.scrollHeight;

            // Update chat state
            chatState = data.state;
        }
    })
    .catch(error => console.error('Error:', error));
}
