let currentConversation = null;

// 创建新对话
function createNewConversation() {
    const id = Date.now().toString(); // 唯一 ID
    const button = document.createElement('button');
    button.textContent = `对话 ${id.slice(-4)}`;
    button.onclick = () => selectConversation(id);
    button.oncontextmenu = (e) => {
        e.preventDefault();
        deleteConversation(id, button);
    };
    document.querySelector('.conversation-list').appendChild(button);

    // 设置当前对话
    selectConversation(id);
}

// 删除会话
function deleteConversation(id, button) {
    document.cookie = `conversation-${id}=; path=/; max-age=0`; // 删除 Cookie
    button.remove();
    if (currentConversation === id) {
        currentConversation = null;
        document.getElementById('messages-container').innerHTML = '';
        disableChat();
    }
}

// 切换会话
function selectConversation(id) {
    currentConversation = id;
    enableChat();

    const messagesContainer = document.getElementById('messages-container');
    messagesContainer.innerHTML = '';

    const chat = loadConversationsFromCookie().find(conv => conv.id === id)?.chat || [];
    chat.forEach(message => addMessageToUI(message.type, message.text));
}

// 添加消息到 UI
function addMessageToUI(type, text) {
    const messageBox = document.createElement('div');
    messageBox.classList.add('message-box');
    if (type === 'ai') {
        messageBox.classList.add('ai');
    } else if (type === 'user') {
        messageBox.classList.add('user');
    }
    messageBox.textContent = text;
    document.getElementById('messages-container').appendChild(messageBox);
}

// 发送消息
async function sendMessage() {
    const inputBox = document.getElementById('inputBox');
    const text = inputBox.value.trim();

    if (!text ||!currentConversation) return;

    // 添加用户消息到 UI
    addMessageToUI('user', text);
    addMessageToUI('ai', ''); // 先添加一个空的 AI 消息框
    const chat = loadConversationsFromCookie().find(conv => conv.id === currentConversation)?.chat || [];
    chat.push({ type: 'user', text });
    saveConversationToCookie(currentConversation, chat);

    inputBox.value = '';
    toggleButtonImage();

    // 发送流式请求到后端获取 AI 回复
    try {
        const response = await fetch('https://spark-api-open.xf-yun.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer FlNLoixiykbsGXdAemOC:rkRUvDmPbNJPBaHboopD', // 替换为你的 API 密钥
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "lite", // 模型选择
                messages: [{ role: "user", content: text }],
                stream: true // 启用流式处理
            })
        });

        if (response.ok) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;
            let aiReply = '';

            // 流式处理每一行响应
            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                aiReply += decoder.decode(value, { stream: true });

                // 添加 AI 回复到 UI
                typewriteMessage(aiReply);
            }

            // 保存会话
            chat.push({ type: 'ai', text: aiReply });
            saveConversationToCookie(currentConversation, chat);
        } else {
            console.error('Error: Failed to get response from AI.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 启用聊天功能
function enableChat() {
    document.getElementById('inputBox').disabled = false;
    document.getElementById('sendButton').disabled = false;
}

// 禁用聊天功能
function disableChat() {
    document.getElementById('inputBox').disabled = true;
    document.getElementById('sendButton').disabled = true;
}

// 页面加载时恢复会话
window.onload = () => {
    loadConversationsFromCookie().forEach(conv => {
        const button = document.createElement('button');
        button.textContent = `对话 ${conv.id.slice(-4)}`;
        button.onclick = () => selectConversation(conv.id);
        button.oncontextmenu = (e) => {
            e.preventDefault();
            deleteConversation(conv.id, button);
        };
        document.querySelector('.conversation-list').appendChild(button);
    });
};

// 从 Cookie 加载会话
function loadConversationsFromCookie() {
    return document.cookie
      .split('; ')  
      .filter(cookie => cookie.startsWith('conversation-'))
      .map(cookie => {
            const [key, value] = cookie.split('=');
            return { id: key.replace('conversation-', ''), chat: JSON.parse(decodeURIComponent(value)) };
        });
}

// 保存会话到 Cookie
function saveConversationToCookie(id, chat) {
    document.cookie = `conversation-${id}=${encodeURIComponent(JSON.stringify(chat))}; path=/; max-age=604800`;
}

// 模拟字符逐个输出的动画
function typewriteMessage(text) {
    const messageBox = document.querySelector('.ai:last-child');
    let i = 0;
    const interval = setInterval(() => {
        if (i < text.length) {
            messageBox.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(interval);
        }
    }, 100); // 调整这个值来控制字符出现的速度
}
