const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = "PASTE-YOUR-API-KEY"; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;

// Options for the user to choose
const options = ["Ticket Booking", "Ticket Cancel", "Train Status", "Download Ticket", "Exit"];

// Function to create chat message list item
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : createOptionsButtons();
    chatLi.innerHTML = chatContent;
    if (className === "incoming") {
        const buttons = chatLi.querySelectorAll(".option-button");
        buttons.forEach((button, index) => {
            button.addEventListener("click", () => handleOptionClick(options[index]));
        });
    }
    return chatLi;
}

// Function to create options buttons
const createOptionsButtons = () => {
    let buttonsHTML = "<div class='options-container'>";
    options.forEach((option, index) => {
        buttonsHTML += `<button class="option-button">${option}</button>`;
    });
    buttonsHTML += "</div>";
    return buttonsHTML;
}

// Function to handle option click
const handleOptionClick = (option) => {
    chatbox.appendChild(createChatLi(option, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    userMessage = option;
    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

// Function to generate response from API
const generateResponse = (chatElement) => {
    const API_URL = "https://api.openai.com/v1/chat/completions";
    const messageElement = chatElement.querySelector("p");
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{role: "user", content: userMessage}],
        })
    }
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        messageElement.textContent = data.choices[0].message.content.trim();
    }).catch(() => {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

// Event listener for input textarea
chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Event listener for send button click
sendChatBtn.addEventListener("click", () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    setTimeout(() => {
        chatbox.appendChild(createChatLi("Please select an option:", "incoming"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }, 600);
});

// Event listeners for close button and chatbot toggler
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
