import './message.css';

export function showMessage(message, type = 'info') {
    const container = document.getElementById('message-container') || createContainer();
    
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-item message-${type}`;
    msgDiv.textContent = message;
    
    container.appendChild(msgDiv);
    
    // Trigger reflow
    void msgDiv.offsetWidth;
    msgDiv.classList.add('show');

    setTimeout(() => {
        msgDiv.classList.remove('show');
        setTimeout(() => {
            msgDiv.remove();
            if (container.children.length === 0) {
                container.remove();
            }
        }, 300);
    }, 3000);
}

function createContainer() {
    const container = document.createElement('div');
    container.id = 'message-container';
    document.body.appendChild(container);
    return container;
}
