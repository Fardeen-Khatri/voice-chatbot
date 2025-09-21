import streamlit as st
import time

# Configure page
st.set_page_config(
    page_title="Personal Voice Assistant", 
    page_icon="🎤",
    layout="centered"
)

# Personal responses database - YOUR CUSTOMIZED RESPONSES
PERSONAL_RESPONSES = {
   "life story": "I'm a mechanical engineer at heart, and you might be thinking why I am here then looking for AI roles, the story begins during the final year of my engineering tenure during which i was told by my faculties that in todays world only theory and bookish knowledge is not enough to survive in corporate world computer knowledge is a must so after my B.E. I joined a course in Data Analytics and Data Science, I learned a lot from building interactive dashboards to machine learning, what i feel is that though my B.E. is in mechanical engineering but the field of AI is such that it can be integrated into any existing field, one such example i can give that in automobile sector there are a lot of data the technical specs, ownership, etc, these are very few each for understanding each of this data as mechanical engineer there is a possibility that I would pocess much better knowledge as compared to than that of a person from a complete IT background thus allowing me to gather and use much more releval=nt information, also i have completed my MBA recently which helps me understand much better how business run domestic as well as international",
    
    "superpower": "My #1 superpower is systematic problem-solving. I approach every challenge methodically, whether it's debugging code, researching the best fuel for my motorcycle, or current AI trends.",
    
    "growth areas": "The top 3 areas I'd like to grow in are: 1) Advanced machine learning algorithms and deep learning, 2) Leadership and mentoring skills as I progress in my career, and 3) Public speaking and presentation skills for technical topics.",
    
    "misconception": "A common misconception that people have that they think i am weak, they take my silence for granted, they think I am incapable to achieve something in life",
    
    "boundaries": "I push my boundaries by trying to stay away from comfort zone, by continuous learning and research."

def get_response(user_input):
    """Generate response based on user input"""
    user_input_lower = user_input.lower()
    
    # Check for keywords in user input
    if any(keyword in user_input_lower for keyword in ["life story", "tell me about yourself", "who are you", "background", "journey"]):
        return PERSONAL_RESPONSES["life story"]
    elif any(keyword in user_input_lower for keyword in ["superpower", "strength", "best at", "good at", "skill"]):
        return PERSONAL_RESPONSES["superpower"] 
    elif any(keyword in user_input_lower for keyword in ["growth", "improve", "develop", "learn", "areas"]):
        return PERSONAL_RESPONSES["growth areas"]
    elif any(keyword in user_input_lower for keyword in ["misconception", "misunderstand", "wrong about", "think about"]):
        return PERSONAL_RESPONSES["misconception"]
    elif any(keyword in user_input_lower for keyword in ["boundaries", "limits", "challenge", "push"]):
        return PERSONAL_RESPONSES["boundaries"]
    else:
        return f"That's an interesting question! I'm designed to answer specific questions about my life story, superpowers, growth areas, misconceptions, and how I push boundaries. What would you like to know more about?"

# Main app
def main():
    st.title("🎤 Personal Voice Assistant")
    st.markdown("Ask me about my life story, superpowers, growth areas, misconceptions, or how I push boundaries!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    
    # Voice interface FIRST
    st.markdown("### 🎙️ Primary Voice Interface")
    st.markdown("*Recommended: Use voice for the best experience!*")
    
    # HTML/JavaScript for voice functionality
    voice_html = f"""
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
    const responses = {{
        "life story": `{PERSONAL_RESPONSES["life story"]}`,
        "superpower": `{PERSONAL_RESPONSES["superpower"]}`,
        "growth": `{PERSONAL_RESPONSES["growth areas"]}`,
        "misconception": `{PERSONAL_RESPONSES["misconception"]}`,
        "boundaries": `{PERSONAL_RESPONSES["boundaries"]}`
    }};
    
    function initSpeechRecognition() {{
        if ('webkitSpeechRecognition' in window) {{
            recognition = new webkitSpeechRecognition();
        }} else if ('SpeechRecognition' in window) {{
            recognition = new SpeechRecognition();
        }} else {{
            document.getElementById('status').innerHTML = '❌ Speech recognition not supported in this browser. Please use Chrome for best experience.';
            return false;
        }}
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {{
            document.getElementById('status').innerHTML = '🎤 Listening... Speak now!';
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            isRecording = true;
        }};
        
        recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById('transcript').innerHTML = '<strong>You said:</strong> ' + transcript;
            
            // Generate response
            const response = generateResponse(transcript);
            currentResponse = response;
            document.getElementById('response').innerHTML = '<strong>Assistant:</strong> ' + response;
            
            document.getElementById('status').innerHTML = '✅ Processing complete! Click "Speak Response" to hear the answer.';
        }};
        
        recognition.onerror = function(event) {{
            let errorMsg = 'Error occurred: ';
            switch(event.error) {{
                case 'no-speech':
                    errorMsg += 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMsg += 'No microphone found. Please check your microphone.';
                    break;
                case 'not-allowed':
                    errorMsg += 'Microphone permission denied. Please allow microphone access.';
                    break;
                default:
                    errorMsg += event.error;
            }}
            document.getElementById('status').innerHTML = '❌ ' + errorMsg;
            resetButtons();
        }};
        
        recognition.onend = function() {{
            resetButtons();
            if (isRecording && document.getElementById('transcript').innerHTML === '') {{
                document.getElementById('status').innerHTML = '🔄 No speech detected. Click "Start Speaking" to try again.';
            }}
        }};
        
        return true;
    }}
    
    function generateResponse(input) {{
        const lowerInput = input.toLowerCase();
        
        if (lowerInput.includes('life story') || lowerInput.includes('tell me about yourself') || lowerInput.includes('who are you') || lowerInput.includes('background') || lowerInput.includes('journey')) {{
            return responses["life story"];
        }} else if (lowerInput.includes('superpower') || lowerInput.includes('strength') || lowerInput.includes('best at') || lowerInput.includes('good at') || lowerInput.includes('skill')) {{
            return responses["superpower"];
        }} else if (lowerInput.includes('growth') || lowerInput.includes('improve') || lowerInput.includes('develop') || lowerInput.includes('learn') || lowerInput.includes('areas')) {{
            return responses["growth"];
        }} else if (lowerInput.includes('misconception') || lowerInput.includes('misunderstand') || lowerInput.includes('wrong about') || lowerInput.includes('think about')) {{
            return responses["misconception"];
        }} else if (lowerInput.includes('boundaries') || lowerInput.includes('limits') || lowerInput.includes('challenge') || lowerInput.includes('push')) {{
            return responses["boundaries"];
        }} else {{
            return "That's an interesting question! I'm designed to answer questions about my life story, superpowers, growth areas, misconceptions, and how I push boundaries. What would you like to know about?";
        }}
    }}
    
    function startRecording() {{
        if (!recognition && !initSpeechRecognition()) {{
            return;
        }}
        
        document.getElementById('transcript').innerHTML = '';
        document.getElementById('response').innerHTML = '';
        currentResponse = '';
        recognition.start();
    }}
    
    function stopRecording() {{
        if (recognition && isRecording) {{
            recognition.stop();
            isRecording = false;
        }}
    }}
    
    function speakResponse() {{
        if (!currentResponse) {{
            document.getElementById('status').innerHTML = '❌ No response to speak. Please ask a question first.';
            return;
        }}
        
        if ('speechSynthesis' in window) {{
            // Stop any ongoing speech
            speechSynthesis.cancel();
            
            // Split long responses into chunks to avoid cutoff
            const maxLength = 200;
            const chunks = currentResponse.match(new RegExp(`.{{1,${{maxLength}}}}(\\s|$)`, 'g')) || [currentResponse];
            
            let chunkIndex = 0;
            
            function speakNextChunk() {{
                if (chunkIndex < chunks.length) {{
                    const utterance = new SpeechSynthesisUtterance(chunks[chunkIndex]);
                    utterance.rate = 0.9;
                    utterance.pitch = 1;
                    utterance.volume = 0.8;
                    
                    utterance.onstart = function() {{
                        document.getElementById('status').innerHTML = `🔊 Speaking response... (${{chunkIndex + 1}}/${{chunks.length}})`;
                    }};
                    
                    utterance.onend = function() {{
                        chunkIndex++;
                        setTimeout(speakNextChunk, 500); // Small pause between chunks
                    }};
                    
                    utterance.onerror = function() {{
                        document.getElementById('status').innerHTML = '❌ Error speaking response';
                    }};
                    
                    speechSynthesis.speak(utterance);
                }} else {{
                    document.getElementById('status').innerHTML = '✅ Response completed!';
                }}
            }}
            
            speakNextChunk();
        }} else {{
            document.getElementById('status').innerHTML = '❌ Text-to-speech not supported in this browser';
        }}
    }}
    
    function resetButtons() {{
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        isRecording = false;
    }}
    
    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', function() {{
        if (initSpeechRecognition()) {{
            document.getElementById('status').innerHTML = '🎤 Ready! Click "Start Speaking" to begin.';
        }}
    }});
    </script>
    """
    
    st.components.v1.html(voice_html, height=450)
    
    # Separator
    st.markdown("---")
    
    # Text input section SECOND (as fallback option)
    st.markdown("### ⌨️ Alternative Text Input")
    st.markdown("*Use this if voice is not available on your device*")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Text input with unique key to prevent infinite loops
        user_input = st.text_input(
            "Type your question here:", 
            key=f"text_input_{st.session_state.input_key}",
            placeholder="Ask me anything about my background...",
            help="This is a fallback option if voice doesn't work on your device"
        )
    
    with col2:
        # Submit button for better UX
        submit_btn = st.button("📤 Submit", key="submit_btn")
    
    # Process text input
    if (user_input and user_input.strip()) or submit_btn:
        if user_input and user_input.strip():
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Generate response
            with st.spinner("Thinking..."):
                response = get_response(user_input)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Increment key to reset input field
            st.session_state.input_key += 1
            
            # Rerun to show new messages and clear input
            st.rerun()
        elif submit_btn and not user_input.strip():
            st.warning("Please enter a question before submitting!")
    
    # Chat History Section - MOVED TO BOTTOM
    if st.session_state.messages:
        st.markdown("---")
        st.markdown("### 💬 Chat History")
        
        # Display chat messages in a container
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
    # Footer section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Clear button
        if st.button("🗑️ Clear Chat History", key="clear_btn"):
            st.session_state.messages = []
            st.session_state.input_key += 1
            st.rerun()
    
    with col2:
        # Instructions button
        with st.expander("📖 How to Use"):
            st.markdown("""
            **Voice Input (Recommended):**
            1. Click "🎤 Start Speaking"
            2. Allow microphone access if prompted
            3. Ask your question clearly
            4. Click "🔊 Speak Response" to hear the answer
            
            **Text Input (Fallback):**
            1. Type your question in the text box
            2. Click "📤 Submit" or press Enter
            
            **Sample Questions:**
            - "Tell me about your life story"
            - "What's your superpower?"
            - "What areas do you want to grow in?"
            - "What misconception do people have about you?"
            - "How do you push your boundaries?"
            """)

if __name__ == "__main__":
    main()
