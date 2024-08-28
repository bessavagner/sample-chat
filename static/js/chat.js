document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chatBox");
    const messageInput = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");
    const ws = new WebSocket(`ws://${window.location.origin.split("://")[1]}/ws`);
    const MAX_MESSAGE_SIZE = 2048;

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === "message") {
            addMessageToChat(data.content, data.from);
        }
    };

    sendButton.addEventListener("click", () => {
        sendMessage();
    });
    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {

            if (new Blob([message]).size > MAX_MESSAGE_SIZE) {
                alert('Message is too long. Please shorten your message.');
                return;
            }
            ws.send(JSON.stringify({ type: "message", content: message }));
            addMessageToChat(message, "you");
            messageInput.value = "";
        }
    }

    function addMessageToChat(message, sender) {
        const messageElement = document.createElement("div");
        let bgColor, textColor, align;
        if (sender === "you") {
            bgColor = "bg-teal-800";
            textColor = "text-neutral-900";
            align = "text-right";
        } else {
            bgColor = "bg-gray-100";
            textColor = "text-gray-700";
            align = "text-left";
        }
        messageElement.textContent = message;
        messageElement.className = `z-10 p-2 mb-2 ${align} rounded-lg ${bgColor} ${textColor}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    document.getElementById('scrollLink').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('panel').scrollIntoView({
            behavior: 'smooth'
        });
    });
});
