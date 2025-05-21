document.addEventListener('DOMContentLoaded', () => {
    // Constants
    const TPC_H = 'TPC-H';
    
    // DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');
    const loginOverlay = document.getElementById('login-overlay');
    const appContainer = document.getElementById('app-container');
    const userIdInput = document.getElementById('user-id-input');
    const loginButton = document.getElementById('login-button');
    const loginError = document.getElementById('login-error');

    // API endpoint
    const API_URL = '/api/chat';
    
    // Session ID (unique for each user session)
    const sessionId = 'session_' + Date.now();
    
    // User ID (set to TPC-H constant)
    let userId = TPC_H;
    
    // Ensure the app starts in login state
    loginOverlay.classList.remove('hidden');
    appContainer.classList.add('hidden');

    // Login handling
    loginButton.addEventListener('click', handleLogin);
    userIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleLogin();
        }
    });

    function handleLogin() {
        console.log("Login button clicked");
        const enteredUserId = userIdInput.value.trim();
        
        if (enteredUserId === TPC_H) {
            // Valid user ID
            userId = enteredUserId;
            loginOverlay.classList.add('hidden');
            appContainer.classList.remove('hidden');
            userInput.focus();
        } else {
            // Invalid user ID
            loginError.textContent = 'Access denied. Invalid client ID.';
            userIdInput.value = '';
            
            // Attempt to close window after delay
            setTimeout(() => {
                try {
                    window.close();
                } catch (e) {
                    // If window.close() fails, display a message and disable the form
                    loginError.textContent = 'Access denied. Please close this window.';
                    userIdInput.disabled = true;
                    loginButton.disabled = true;
                    // Hide any existing content
                    appContainer.classList.add('hidden');
                }
            }, 3000);
        }
    }

    // Add event listener for form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Check if user is logged in
        if (!userId) {
            alert("Please login first with a valid client ID.");
            return;
        }
        
        // Get user input
        const message = userInput.value.trim();
        
        // Check if message is empty
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Disable input and button while waiting for response
        toggleInputState(true);
        
        try {
            // Send message to API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message,
                    session_id: sessionId,
                    user_id: userId
                }),
            });
            
            // Check if response is ok
            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }
            
            // Parse response
            const data = await response.json();
            
            // Add agent response to chat
            addMessage(data.response, 'agent');
            
        } catch (error) {
            console.error('Error:', error);
            
            // Add error message to chat
            addMessage('Sorry, there was an error processing your request. Please try again.', 'system');
        } finally {
            // Re-enable input and button
            toggleInputState(false);
            
            // Scroll to bottom of chat
            scrollToBottom();
        }
    });

    // Function to add a message to the chat
    function addMessage(content, sender) {
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        // Create message content element
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Format the content (handle code blocks)
        const formattedContent = formatContent(content);
        messageContent.innerHTML = formattedContent;
        
        // Add message content to message
        messageDiv.appendChild(messageContent);
        
        // Add message to chat
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom of chat
        scrollToBottom();
    }

    // Function to format content (handle code blocks and Markdown)
    function formatContent(content) {
        // Replace code blocks
        let formatted = content.replace(/```yaml\s*([\s\S]*?)\s*```/g, '<pre><code>$1</code></pre>');
        
        // Replace line breaks with <br>
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }

    // Function to toggle input state
    function toggleInputState(disabled) {
        userInput.disabled = disabled;
        sendButton.disabled = disabled;
    }

    // Function to scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Focus input on login
    userIdInput.focus();
}); 