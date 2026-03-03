/**
 * ═══════════════════════════════════════════════════════════════
 * Voice-Controlled LLM App — Frontend Application Logic
 * Handles recording, playback, API calls, and chat UI state
 * ═══════════════════════════════════════════════════════════════
 */

// ─── State ───
const state = {
    isRecording: false,
    isProcessing: false,
    mediaRecorder: null,
    audioChunks: [],
    messages: [],
};

// ─── DOM References ───
const dom = {
    chatArea: document.getElementById('chat-area'),
    emptyState: document.getElementById('empty-state'),
    textInput: document.getElementById('text-input'),
    sendBtn: document.getElementById('btn-send'),
    recordBtn: document.getElementById('btn-record'),
    uploadBtn: document.getElementById('btn-upload'),
    fileInput: document.getElementById('file-upload'),
    typingIndicator: document.getElementById('typing-indicator'),
    waveform: document.getElementById('waveform'),
    statusDot: document.getElementById('status-dot'),
    statusText: document.getElementById('status-text'),
    settingsToggle: document.getElementById('settings-toggle'),
    settingsPanel: document.getElementById('settings-panel'),
    settingsOverlay: document.getElementById('settings-overlay'),
    clearBtn: document.getElementById('btn-clear'),
};

// ─── Initialize ───
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    autoResizeTextarea();
    loadSettings();
});

function setupEventListeners() {
    // Send message
    dom.sendBtn.addEventListener('click', handleSendText);
    dom.textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendText();
        }
    });

    // Auto-resize textarea
    dom.textInput.addEventListener('input', autoResizeTextarea);

    // Record audio
    dom.recordBtn.addEventListener('click', toggleRecording);

    // Upload audio
    dom.uploadBtn.addEventListener('click', () => dom.fileInput.click());
    dom.fileInput.addEventListener('change', handleFileUpload);

    // Settings
    dom.settingsToggle.addEventListener('click', toggleSettings);
    dom.settingsOverlay.addEventListener('click', toggleSettings);

    // Clear conversation
    dom.clearBtn.addEventListener('click', clearConversation);

    // Hint chips
    document.querySelectorAll('.hint-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            dom.textInput.value = chip.textContent;
            autoResizeTextarea();
            handleSendText();
        });
    });
}

// ─── Text Input ───
function autoResizeTextarea() {
    dom.textInput.style.height = 'auto';
    dom.textInput.style.height = Math.min(dom.textInput.scrollHeight, 120) + 'px';
    dom.sendBtn.disabled = !dom.textInput.value.trim() && !state.isRecording;
}

async function handleSendText() {
    const text = dom.textInput.value.trim();
    if (!text || state.isProcessing) return;

    addMessage('user', text);
    dom.textInput.value = '';
    autoResizeTextarea();

    await processWithAPI('/api/chat', { text });
}

// ─── Audio Recording ───
async function toggleRecording() {
    if (state.isRecording) {
        stopRecording();
    } else {
        await startRecording();
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        state.mediaRecorder = new MediaRecorder(stream, {
            mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4'
        });
        state.audioChunks = [];

        state.mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) state.audioChunks.push(e.data);
        };

        state.mediaRecorder.onstop = async () => {
            stream.getTracks().forEach(track => track.stop());
            const blob = new Blob(state.audioChunks, { type: state.mediaRecorder.mimeType });
            await handleAudioBlob(blob);
        };

        state.mediaRecorder.start(250); // Collect data every 250ms
        state.isRecording = true;
        updateRecordingUI(true);

    } catch (err) {
        console.error('Microphone access denied:', err);
        showToast('Microphone access denied. Please allow microphone permissions.');
    }
}

function stopRecording() {
    if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
        state.mediaRecorder.stop();
    }
    state.isRecording = false;
    updateRecordingUI(false);
}

function updateRecordingUI(recording) {
    dom.recordBtn.classList.toggle('recording', recording);
    dom.recordBtn.innerHTML = recording ? '⏹' : '🎤';
    dom.waveform.classList.toggle('active', recording);
    dom.statusDot.className = recording ? 'status-dot status-dot--recording' : 'status-dot';
    dom.statusText.textContent = recording ? 'Recording...' : 'Ready';
}

// ─── Audio Upload ───
function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    handleAudioBlob(file);
    dom.fileInput.value = ''; // Reset file input
}

async function handleAudioBlob(blob) {
    addMessage('user', '🎤 Audio message sent');
    setStatus('processing', 'Transcribing...');

    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');

    await processWithAPI('/api/transcribe', formData, true);
}

// ─── API Communication ───
async function processWithAPI(endpoint, data, isFormData = false) {
    state.isProcessing = true;
    showTypingIndicator(true);
    setStatus('processing', 'Processing...');

    try {
        const options = {
            method: 'POST',
        };

        if (isFormData) {
            options.body = data;
        } else {
            options.headers = { 'Content-Type': 'application/json' };
            options.body = JSON.stringify(data);
        }

        const response = await fetch(endpoint, options);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        // For transcribed audio, update the last user message with transcription
        if (result.transcription) {
            updateLastUserMessage(`🎤 "${result.transcription}"`);
        }

        // Add AI response
        addMessage('assistant', result.response, result.audio_url);

    } catch (err) {
        console.error('API Error:', err);
        addMessage('assistant', 'Sorry, an error occurred while processing your request. Please try again.');
    } finally {
        state.isProcessing = false;
        showTypingIndicator(false);
        setStatus('ready', 'Ready');
    }
}

// ─── Chat UI ───
function addMessage(role, content, audioUrl = null) {
    // Hide empty state
    if (dom.emptyState) {
        dom.emptyState.style.display = 'none';
    }

    const msgEl = document.createElement('div');
    msgEl.className = `message message--${role}`;

    const avatarEmoji = role === 'user' ? '👤' : '🤖';

    let audioHTML = '';
    if (audioUrl) {
        audioHTML = `
            <div class="message__audio">
                <audio controls preload="auto">
                    <source src="${audioUrl}" type="audio/mpeg">
                </audio>
            </div>
        `;
    }

    msgEl.innerHTML = `
        <div class="message__avatar">${avatarEmoji}</div>
        <div class="message__content">
            <div class="message__bubble">${escapeHTML(content)}</div>
            ${audioHTML}
        </div>
    `;

    dom.chatArea.appendChild(msgEl);
    scrollToBottom();

    // Store in state
    state.messages.push({ role, content, audioUrl });
}

function updateLastUserMessage(content) {
    const userMessages = dom.chatArea.querySelectorAll('.message--user');
    if (userMessages.length > 0) {
        const lastMsg = userMessages[userMessages.length - 1];
        const bubble = lastMsg.querySelector('.message__bubble');
        if (bubble) bubble.textContent = content;
    }
}

function showTypingIndicator(show) {
    dom.typingIndicator.classList.toggle('active', show);
    if (show) scrollToBottom();
}

function scrollToBottom() {
    dom.chatArea.scrollTop = dom.chatArea.scrollHeight;
}

// ─── Settings ───
function toggleSettings() {
    dom.settingsPanel.classList.toggle('open');
    dom.settingsOverlay.classList.toggle('active');
}

async function loadSettings() {
    try {
        const response = await fetch('/api/settings');
        if (response.ok) {
            const settings = await response.json();
            document.getElementById('setting-model').textContent = settings.model || 'gpt-3.5-turbo';
            document.getElementById('setting-temperature').textContent = settings.temperature || '0.7';
            document.getElementById('setting-max-tokens').textContent = settings.max_tokens || '150';
            document.getElementById('setting-voice').textContent = settings.voice || 'alloy';
        }
    } catch (err) {
        console.log('Settings not available yet');
    }
}

function clearConversation() {
    state.messages = [];
    dom.chatArea.innerHTML = '';

    // Show empty state again
    if (dom.emptyState) {
        dom.emptyState.style.display = '';
        dom.chatArea.appendChild(dom.emptyState);
    }

    toggleSettings();

    // Notify server to clear memory
    fetch('/api/clear', { method: 'POST' }).catch(() => { });
}

// ─── Status ───
function setStatus(type, text) {
    dom.statusDot.className = `status-dot${type === 'processing' ? ' status-dot--processing' : type === 'recording' ? ' status-dot--recording' : ''}`;
    dom.statusText.textContent = text;
}

// ─── Utilities ───
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function showToast(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
        background: rgba(239, 68, 68, 0.9); color: white;
        padding: 0.75rem 1.5rem; border-radius: 0.5rem;
        font-size: 0.85rem; z-index: 9999;
        animation: message-in 0.35s ease-out;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}
