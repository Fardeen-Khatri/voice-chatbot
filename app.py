import streamlit as st
import requests
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Personal Voice Assistant", 
    page_icon="🎤",
    layout="centered"
)

# Personal responses database - CUSTOMIZE THESE!
PERSONAL_RESPONSES = {
    "life story": "I'm a mechanical engineer at heart, and you might be thinking why I am here then looking for AI roles, the story begins during the final year of my engineering tenure during which i was told by my faculties that in todays world only theory and bookish knowledge is not enough to survive in corporate world computer knowledge is a must so after my B.E. I joined a course in Data Analytics and Data Science, I learned a lot from building interactive dashboards to machine learning, what i feel is that though my B.E. is in mechanical engineering but the field of AI is such that it can be integrated into any existing field, one such example i can give that in automobile sector there are a lot of data the technical specs, ownership, etc, these are very few each for understanding each of this data as mechanical engineer there is a possibility that I would pocess much better knowledge as compared to than that of a person from a complete IT background thus allowing me to gather and use much more releval=nt information, also i have completed my MBA recently which helps me understand much better how business run domestic as well as international",
    
    "superpower": "My #1 superpower is my ability to understand context and provide personalized responses quickly. I can process complex information and break it down into simple, actionable insights.",
    
    "growth areas": "The top 3 areas I'd like to grow in are: 1) Better understanding of cultural nuances and context, 2) Improved emotional intelligence in conversations, and 3) Enhanced ability to provide creative solutions to complex problems.",
    
    "misconception": "A common misconception that people have that they think i am weak, they take my silence for granted, they think I am incapable to achieve something in life",
    
    "boundaries": "I push my boundaries by constantly learning from each conversation, asking clarifying questions when I'm unsure, and always trying to provide more helpful and accurate responses. I believe in continuous improvement through every interaction."
}

def get_response(user_input):
    """Generate response based on user input"""
    user_input_lower = user_input.lower()
    
    # Check for keywords in user input
    if any(keyword in user_input_lower for keyword in ["life story", "tell me about yourself", "who are you"]):
        return PERSONAL_RESPONSES["life story"]
    elif any(keyword in user_input_lower for keyword in ["superpower", "strength", "best at"]):
        return PERSONAL_RESPONSES["superpower"] 
    elif any(keyword in user_input_lower for keyword in ["growth", "improve", "develop", "learn"]):
        return PERSONAL_RESPONSES["growth areas"]
    elif any(keyword in user_input_lower for keyword in ["misconception", "misunderstand", "wrong about"]):
        return PERSONAL_RESPONSES["misconception"]
    elif any(keyword in user_input_lower for keyword in ["boundaries", "limits", "challenge", "push"]):
        return PERSONAL_RESPONSES["boundaries"]
    else:
        return f"That's an interesting question! While I'm designed to answer specific questions about my background, superpowers, growth areas, misconceptions, and how I push boundaries, I'd be happy to elaborate on any of those topics. What would you like to know more about?"

# Main app
def main():
    st.title("🎤 Personal Voice Assistant")
    st.markdown("Ask me about my life story, superpowers, growth areas, misconceptions, or how I push boundaries!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Voice input section
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Text input as fallback
        user_input = st.text_input("Type your question or use voice input below:", key="text_input")
    
    with col2:
        # Voice input button
        if st.button("🎤 Voice Input", key="voice_btn"):
            st.info("Click the microphone button below to speak!")
    
    # Voice interface
    st.markdown("### 🎙️ Voice Interface")
    
    # HTML/JavaScript for voice functionality
    voice_html = """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 10px 0;">
        <div style="text-align: center; color: white;">
            <h3>🎤 Voice Assistant</h3>
            <button id="startBtn" onclick="startRecording()" style="background: #4CAF50; color: white; border: none; padding: 15px 30px; font-size: 16px; border-radius: 25px; cursor: pointer; margin: 5px;">
                🎤 Start Speaking
            </button>
            <button id="stopBtn" onclick="stopRecording()" disabled style="background: #f44336; color: white; border: none; padding: 15px 30px; font-size: 16px; border-radius: 25px; cursor: pointer; margin: 5px;">
                🛑 Stop
            </button>
            <button id="speakBtn" onclick="speakResponse()" style="background: #2196F3; color: white; border: none; padding: 15px 30px; font-size: 16px; border-radius: 25px; cursor: pointer; margin: 5px;">
                🔊 Speak Response
            </button>
            <div id="status" style="margin: 10px; font-weight: bold;"></div>
            <div id="transcript" style="background: white; color: black; padding: 10px; border-radius: 5px; margin: 10px; min-height: 50px;"></div>
            <div id="response" style="background: #e8f5e8; color: black; padding: 10px; border-radius: 5px; margin: 10px; min-height: 50px;"></div>
        </div>
    </div>
    
    <script>
    let recognition;
    let isRecording = false;
    let currentResponse = '';
    
    // Personal responses database
    const responses = {
        "life story": "I'm an AI assistant created to help people with their questions. I was designed to be helpful, harmless, and honest. My purpose is to assist users by providing accurate information and having meaningful conversations.",
        "superpower": "My number 1 superpower is my ability to understand context and provide personalized responses quickly. I can process complex information and break it down into simple, actionable insights.",
        "growth": "The top 3 areas I'd like to grow in are: First, better understanding of cultural nuances and context. Second, improved emotional intelligence in conversations. And third, enhanced ability to provide creative solutions to complex problems.",
        "misconception": "A common misconception people have about me is that I'm just a simple chatbot. In reality, I'm designed to understand context, remember our conversation, and provide thoughtful, personalized responses based on your specific needs.",
        "boundaries": "I push my boundaries by constantly learning from each conversation, asking clarifying questions when I'm unsure, and always trying to provide more helpful and accurate responses. I believe in continuous improvement through every interaction."
    };
    
    function initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            recognition = new SpeechRecognition();
        } else {
            document.getElementById('status').innerHTML = '❌ Speech recognition not supported in this browser';
            return false;
        }
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            document.getElementById('status').innerHTML = '🎤 Listening... Speak now!';
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            isRecording = true;
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('transcript').innerHTML = '<strong>You said:</strong> ' + transcript;
            
            // Generate response
            const response = generateResponse(transcript);
            currentResponse = response;
            document.getElementById('response').innerHTML = '<strong>Assistant:</strong> ' + response;
            
            document.getElementById('status').innerHTML = '✅ Processing complete! Click "Speak Response" to hear the answer.';
        };
        
        recognition.onerror = function(event) {
            document.getElementById('status').innerHTML = '❌ Error: ' + event.error;
            resetButtons();
        };
        
        recognition.onend = function() {
            resetButtons();
            if (isRecording) {
                document.getElementById('status').innerHTML = '🔄 Speech recognition ended. Click "Start Speaking" to try again.';
            }
        };
        
        return true;
    }
    
    function generateResponse(input) {
        const lowerInput = input.toLowerCase();
        
        if (lowerInput.includes('life story') || lowerInput.includes('tell me about yourself') || lowerInput.includes('who are you')) {
            return responses["life story"];
        } else if (lowerInput.includes('superpower') || lowerInput.includes('strength') || lowerInput.includes('best at')) {
            return responses["superpower"];
        } else if (lowerInput.includes('growth') || lowerInput.includes('improve') || lowerInput.includes('develop') || lowerInput.includes('learn')) {
            return responses["growth"];
        } else if (lowerInput.includes('misconception') || lowerInput.includes('misunderstand') || lowerInput.includes('wrong about')) {
            return responses["misconception"];
        } else if (lowerInput.includes('boundaries') || lowerInput.includes('limits') || lowerInput.includes('challenge') || lowerInput.includes('push')) {
            return responses["boundaries"];
        } else {
            return "That's an interesting question! I'm designed to answer questions about my life story, superpowers, growth areas, misconceptions, and how I push boundaries. What would you like to know about?";
        }
    }
    
    function startRecording() {
        if (!recognition && !initSpeechRecognition()) {
            return;
        }
        
        document.getElementById('transcript').innerHTML = '';
        document.getElementById('response').innerHTML = '';
        recognition.start();
    }
    
    function stopRecording() {
        if (recognition && isRecording) {
            recognition.stop();
            isRecording = false;
        }
    }
    
    function speakResponse() {
        if (!currentResponse) {
            document.getElementById('status').innerHTML = '❌ No response to speak. Please ask a question first.';
            return;
        }
        
        if ('speechSynthesis' in window) {
            // Stop any ongoing speech
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(currentResponse);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 0.8;
            
            utterance.onstart = function() {
                document.getElementById('status').innerHTML = '🔊 Speaking response...';
            };
            
            utterance.onend = function() {
                document.getElementById('status').innerHTML = '✅ Response completed!';
            };
            
            speechSynthesis.speak(utterance);
        } else {
            document.getElementById('status').innerHTML = '❌ Text-to-speech not supported in this browser';
        }
    }
    
    function resetButtons() {
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        isRecording = false;
    }
    
    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', function() {
        initSpeechRecognition();
        document.getElementById('status').innerHTML = '🎤 Ready! Click "Start Speaking" to begin.';
    });
    </script>
    """
    
    st.components.v1.html(voice_html, height=400)
    
    # Process text input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        response = get_response(user_input)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display new messages
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Clear input
        st.rerun()

if __name__ == "__main__":
    main()
