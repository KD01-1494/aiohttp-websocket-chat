let clientWebSocket = new WebSocket('ws://localhost:8800/websocketChat');

clientWebSocket.onopen = (e) => {
  console.log('[Open chat connection]');
  chatInsertHandler();
};
clientWebSocket.onсlose = (e) => {
  console.log(`[Close chat connection] ${e.data}`);
};

clientWebSocket.onmessage = (e) => {
  let data = JSON.parse(e.data);
  appendChatWindowMessage(data['messageAuthor'], data['messageText']);
};

let appendChatWindowMessage = (name, message) => {
  let chatWindow = document.querySelector('.chat-window');
  let html = `
    <div class="chat-message">
        <p class="chat-message-author">${name}:&nbsp;</p>
        <p class="chat-message-text">${message}</p>
    </div>
  `;
  chatWindow.insertAdjacentHTML('beforeend', html);
}

let chatInsertHandler = () => {
  let submitChatButton = document.querySelector('.submit-button');
  submitChatButton.addEventListener('click', () => {
    let message = document.querySelector('.message-box').value;
    clientWebSocket.send(message)
    message = ''
  });
}