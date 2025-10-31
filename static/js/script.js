const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    // Display user message
    const userMsg = document.createElement("div");
    userMsg.className = "user-message";
    userMsg.textContent = message;
    chatBox.appendChild(userMsg);
    userInput.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    // 🩷 Show typing indicator
    const typingMsg = document.createElement("div");
    typingMsg.className = "bot-message typing";
    typingMsg.textContent = "ChinguBot is typing...";
    chatBox.appendChild(typingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        // Remove typing message
        chatBox.removeChild(typingMsg);

        // Show bot reply
        const botMsg = document.createElement("div");
        botMsg.className = "bot-message";
        botMsg.textContent = data.reply;
        chatBox.appendChild(botMsg);
    } catch (error) {
        chatBox.removeChild(typingMsg);
        const errorMsg = document.createElement("div");
        errorMsg.className = "bot-message";
        errorMsg.textContent = "Oops 😅 Something went wrong. Try again later!";
        chatBox.appendChild(errorMsg);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
