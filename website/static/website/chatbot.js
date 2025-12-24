// Chat state
let chatHistory = []
let isTyping = false;
let attachedFiles = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupInputHandlers();
    checkForTopicParam();
});

// Check if there's a topic or subject from URL parameters
function checkForTopicParam() {
    const urlParams = new URLSearchParams(window.location.search);
    const subject = urlParams.get('subject');
    const topic = urlParams.get('topic');
    
    if (subject) {
        sendMessage(`I want to learn about ${subject}`);
    } else if (topic) {
        sendMessage(`Tell me about ${topic}`);
    }
}

// Setup input handlers
function setupInputHandlers() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        
        // Enable/disable send button
        sendBtn.disabled = this.value.trim() === '';
    });
    
    // Handle Enter key
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Send message

async function sendMessage(messageText = null) {
    const input = document.getElementById("chatInput");
    const message = messageText ?? input.value.trim();

    if (!message && attachedFiles.length === 0) return;
    if (isTyping) return;

    // REMOVE EMPTY / SUGGESTION UI
    document.querySelector(".chat-empty")?.remove();

    // Show user message
    let combinedMessage = message;
    if (attachedFiles.length > 0) {
        combinedMessage += attachedFiles.map(f => `\n📎 ${f.name}`).join("");
    }

    addMessage(combinedMessage || "📎 Sent an attachment", "user");

    input.value = "";
    attachedFiles = [];
    document.getElementById("attachmentPreview")?.remove();

    isTyping = true;

    try {
    const res = await fetch("/api/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    });

    const data = await res.json();

    if (data.success) {
        addMessage(data.bot_response, "ai");
    } else {
        addMessage("⚠️ " + data.message, "ai");
    }
} catch (error) {
    addMessage("⚠️ AI service unavailable.", "ai");
}


    isTyping = false;
}

// Send suggestion
function sendSuggestion(text) {
    sendMessage(text);
}

// Add message to chat
function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar ' + (sender === 'user' ? 'user-avatar' : 'ai-avatar');
    avatar.textContent = sender === 'user' ? 'U' : '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text;
    
    content.appendChild(messageText);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Store in history
    chatHistory.push({ sender, text, timestamp: new Date() });
}

function toggleAttachMenu() {
    const menu = document.getElementById("attachMenu");
    menu.classList.toggle("show");
}

// Close menu when clicking outside
document.addEventListener("click", (e) => {
    const wrapper = document.querySelector(".attach-wrapper");
    if (!wrapper.contains(e.target)) {
        document.getElementById("attachMenu")?.classList.remove("show");
    }
});

// Handle file selection
function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    attachedFiles.push(...files);

    document.getElementById("attachMenu").classList.remove("show");
    showAttachmentPreview();
}
function showAttachmentPreview() {
    let preview = document.getElementById("attachmentPreview");

    if (!preview) {
        preview = document.createElement("div");
        preview.id = "attachmentPreview";
        preview.className = "attachment-preview";
        document.querySelector(".chat-input").prepend(preview);
    }

    preview.innerHTML = attachedFiles.map((file, i) => `
        <div class="attachment-pill">
            📎 ${file.name}
            <span onclick="removeAttachment(${i})">✕</span>
        </div>
    `).join("");
}

// New chat
function newChat() {
    if (chatHistory.length > 0) {
        if (!confirm('Start a new chat? Current conversation will be saved.')) {
            return;
        }
    }
    
    // Clear messages
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.innerHTML = `
        <div class="chat-empty">
            <div class="empty-icon">🤖</div>
            <h2>How can I help you learn today?</h2>
            <p>Ask me anything about your studies, homework, or learning concepts!</p>

            <div class="suggestion-cards">
                <div class="suggestion-card" onclick="sendSuggestion('Explain object-oriented programming concepts')">
                    <div class="suggestion-icon">💡</div>
                    <h3>Explain Concepts</h3>
                    <p>Explain object-oriented programming concepts</p>
                </div>

                <div class="suggestion-card" onclick="sendSuggestion('Help me solve this math problem: 2x + 5 = 15')">
                    <div class="suggestion-icon">📐</div>
                    <h3>Solve Problems</h3>
                    <p>Help me solve this math problem: 2x + 5 = 15</p>
                </div>

                <div class="suggestion-card" onclick="sendSuggestion('Give me study tips for better focus')">
                    <div class="suggestion-icon">📚</div>
                    <h3>Study Tips</h3>
                    <p>Give me study tips for better focus</p>
                </div>

                <div class="suggestion-card" onclick="sendSuggestion('What are the best practices for learning Python?')">
                    <div class="suggestion-icon">🎯</div>
                    <h3>Learning Advice</h3>
                    <p>What are the best practices for learning Python?</p>
                </div>
            </div>
        </div>
    `;
    
    // Save old chat history if needed
    if (chatHistory.length > 0) {
        const savedChats = JSON.parse(sessionStorage.getItem('savedChats') || '[]');
        savedChats.push({
            id: Date.now(),
            timestamp: new Date(),
            messages: [...chatHistory]
        });
        sessionStorage.setItem('savedChats', JSON.stringify(savedChats));
    }
    
    // Reset chat history
    chatHistory = [];
}

// Clear conversations
function clearConversations() {
    if (confirm('Are you sure you want to clear all conversations? This cannot be undone.')) {
        sessionStorage.removeItem('savedChats');
        chatHistory = [];
        newChat();
        alert('All conversations cleared!');
    }
}

// Handle recent chat clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('.chat-item')) {
        const chatItems = document.querySelectorAll('.chat-item');
        chatItems.forEach(item => item.classList.remove('active'));
        e.target.closest('.chat-item').classList.add('active');
    }
});

function removeAttachment(index) {
    attachedFiles.splice(index, 1);
    showAttachmentPreview();
}
