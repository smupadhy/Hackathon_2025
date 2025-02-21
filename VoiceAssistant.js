import React, { useState } from "react";

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.continuous = false; // Only capture one phrase at a time
recognition.lang = "en-US"; // Set language
recognition.interimResults = false; // Don't show partial results
recognition.maxAlternatives = 1; // Give only one final result

function VoiceAssistant() {
  const [text, setText] = useState("");

  // Function to start voice recognition
  const startListening = () => {
    setText("Listening...");
    recognition.start();
  };

  // When speech is recognized
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setText(transcript);
    console.log("User said:", transcript);
    
    // TODO: Connect this with AWS services (Banking features)
  };

  // If there is an error
  recognition.onerror = (event) => {
    console.log("Error occurred in recognition: ", event.error);
    setText("Error: " + event.error);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h2>AI Voice Assistant</h2>
      <button onClick={startListening}> Speak Now</button>
      <p>{text}</p>
    </div>
  );
}

export default VoiceAssistant;
