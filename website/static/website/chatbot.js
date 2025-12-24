// Chat state
let chatHistory = [];
let isTyping = false;
let attachedFiles = [];
let currentConversationId = null;
let userEmail = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupInputHandlers();
    loadUserEmail();
    loadConversations();
    checkForTopicParam();
});

// Load user email from localStorage (set during login)
function loadUserEmail() {
    userEmail = localStorage.getItem('userEmail');
    
    // Fallback to sessionStorage if not in localStorage
    if (!userEmail) {
        const userData = sessionStorage.getItem('user');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                userEmail = user.email;
                // Also save to localStorage for future use
                if (userEmail) {
                    localStorage.setItem('userEmail', userEmail);
                }
            } catch (e) {
                console.error('Error parsing user data:', e);
            }
        }
    }
    
    if (!userEmail) {
        console.log('No user email found. Chat history will not be saved.');
    }
}

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

// Load conversations list from database
async function loadConversations() {
    if (!userEmail) {
        showNoConversations();
        return;
    }

    try {
        const res = await fetch(`/api/conversations/?email=${encodeURIComponent(userEmail)}`);
        const data = await res.json();

        if (data.success && data.data.length > 0) {
            renderConversationsList(data.data);
        } else {
            showNoConversations();
        }
    } catch (error) {
        console.error('Error loading conversations:', error);
        showNoConversations();
    }
}

// Render conversations in sidebar
function renderConversationsList(conversations) {
    const container = document.getElementById('conversationsList');
    container.innerHTML = '';

    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = `conversation-item${currentConversationId === conv.id ? ' active' : ''}`;
        item.dataset.id = conv.id;
        
        item.innerHTML = `
            <span class="conversation-title" title="${escapeHtml(conv.title)}">${escapeHtml(conv.title)}</span>
            <button class="conversation-delete" onclick="deleteConversation(event, ${conv.id})" title="Delete">🗑</button>
        `;
        
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('conversation-delete')) {
                loadConversation(conv.id);
            }
        });
        
        container.appendChild(item);
    });
}

// Show "no conversations" message
function showNoConversations() {
    const container = document.getElementById('conversationsList');
    container.innerHTML = '<div class="no-conversations">No conversations yet</div>';
}

// Create a new conversation
async function createConversation(title = 'New Chat') {
    if (!userEmail) {
        console.log('Cannot create conversation: No user email');
        return null;
    }

    try {
        const res = await fetch('/api/conversations/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail, title: title })
        });

        const data = await res.json();
        
        if (data.success) {
            currentConversationId = data.conversation_id;
            await loadConversations();
            return data.conversation_id;
        }
    } catch (error) {
        console.error('Error creating conversation:', error);
    }
    return null;
}

// Load a specific conversation's messages
async function loadConversation(conversationId) {
    if (!userEmail) return;

    try {
        const res = await fetch(`/api/messages/?email=${encodeURIComponent(userEmail)}&conversation_id=${conversationId}`);
        const data = await res.json();

        if (data.success) {
            currentConversationId = conversationId;
            chatHistory = [];
            
            // Clear chat and render messages
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = '';

            if (data.data.length === 0) {
                // Show empty state if no messages
                showEmptyChat();
            } else {
                data.data.forEach(msg => {
                    const sender = msg.role === 'user' ? 'user' : 'ai';
                    addMessageToUI(msg.content, sender);
                    chatHistory.push({ sender, text: msg.content, timestamp: new Date(msg.created_at) });
                });
            }

            // Update active state in sidebar
            document.querySelectorAll('.conversation-item').forEach(item => {
                item.classList.remove('active');
                if (parseInt(item.dataset.id) === conversationId) {
                    item.classList.add('active');
                }
            });
        }
    } catch (error) {
        console.error('Error loading conversation:', error);
    }
}

// Delete a conversation
async function deleteConversation(event, conversationId) {
    event.stopPropagation();
    
    if (!confirm('Delete this conversation?')) return;
    if (!userEmail) return;

    try {
        const res = await fetch('/api/conversations/', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: userEmail, conversation_id: conversationId })
        });

        const data = await res.json();

        if (data.success) {
            // If we deleted the current conversation, start a new chat
            if (currentConversationId === conversationId) {
                currentConversationId = null;
                chatHistory = [];
                showEmptyChat();
            }
            await loadConversations();
        }
    } catch (error) {
        console.error('Error deleting conversation:', error);
    }
}

// Send message
async function sendMessage(messageText = null) {
    const input = document.getElementById("chatInput");
    const message = messageText ?? input.value.trim();

    if (!message && attachedFiles.length === 0) return;
    if (isTyping) return;

    // REMOVE EMPTY / SUGGESTION UI
    document.querySelector(".chat-empty")?.remove();

    // Create conversation if none exists
    if (!currentConversationId && userEmail) {
        await createConversation(message.substring(0, 50));
    }

    // Show user message
    let combinedMessage = message;
    if (attachedFiles.length > 0) {
        combinedMessage += attachedFiles.map(f => `\n📎 ${f.name}`).join("");
    }

    addMessageToUI(combinedMessage || "📎 Sent an attachment", "user");

    input.value = "";
    input.style.height = 'auto';
    attachedFiles = [];
    document.getElementById("attachmentPreview")?.remove();

    isTyping = true;

    try {
        const res = await fetch("/api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                message: message,
                email: userEmail,
                conversation_id: currentConversationId
            })
        });

        const data = await res.json();

        if (data.success) {
            addMessageToUI(data.bot_response, "ai");
            
            // Update conversation ID if returned
            if (data.conversation_id) {
                currentConversationId = data.conversation_id;
            }
            
            // Refresh conversations list to show updated title
            await loadConversations();
        } else {
            addMessageToUI("⚠️ " + data.message, "ai");
        }
    } catch (error) {
        addMessageToUI("⚠️ AI service unavailable.", "ai");
    }

    isTyping = false;
}

// Send suggestion
function sendSuggestion(text) {
    sendMessage(text);
}

// Add message to UI only (without storing)
function addMessageToUI(text, sender) {
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
    
    // Store in local history
    chatHistory.push({ sender, text, timestamp: new Date() });
}

// Show empty chat state
function showEmptyChat() {
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
}

// New chat
function newChat() {
    currentConversationId = null;
    chatHistory = [];
    showEmptyChat();
    
    // Remove active state from all conversations
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.remove('active');
    });
}

function toggleAttachMenu() {
    const menu = document.getElementById("attachMenu");
    menu.classList.toggle("show");
}

// Close menu when clicking outside
document.addEventListener("click", (e) => {
    const wrapper = document.querySelector(".attach-wrapper");
    if (wrapper && !wrapper.contains(e.target)) {
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

function removeAttachment(index) {
    attachedFiles.splice(index, 1);
    showAttachmentPreview();
}

// Clear all conversations
function clearConversations() {
    if (confirm('Are you sure you want to clear all conversations? This cannot be undone.')) {
        // This would require a backend endpoint to delete all conversations
        // For now, just clear local state
        currentConversationId = null;
        chatHistory = [];
        newChat();
        alert('All conversations cleared!');
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
