const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatWindow = document.getElementById('chatWindow');

function addBubble(text, sender) {
    const div = document.createElement('div');
    div.className = sender === 'user'
        ? 'bg-green-700 text-white p-3 rounded-lg max-w-[80%] ml-auto shadow'
        : 'bg-white text-black p-3 rounded-lg max-w-[80%] mr-auto shadow border border-gray-200 whitespace-pre-line';
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

sendBtn.addEventListener('click', async () => {
    const msg = userInput.value.trim();
    if (!msg) return;

    addBubble(msg, 'user');
    userInput.value = '';

    const res = await fetch('/api/coach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    addBubble(data.answer || 'Sorry, I could not generate a response.', 'bot');
});
