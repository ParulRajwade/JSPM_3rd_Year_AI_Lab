const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function appendMessage(message, className) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", className);
  msgDiv.innerHTML = message
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  chatBox.appendChild(msgDiv);

  // 👇 Auto scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (message === "") return;

  appendMessage(message, "user-message");
  userInput.value = "";

  // temporary typing indicator
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "bot-message");
  typingDiv.textContent = "Typing...";
  chatBox.appendChild(typingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    // remove typing indicator
    typingDiv.remove();

    appendMessage(data.reply, "bot-message");
  } catch (error) {
    typingDiv.remove();
    appendMessage("⚠️ Something went wrong. Try again later.", "bot-message");
  }
}
