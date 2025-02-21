import React, { useState } from "react";
import WakeWordListener from "./WakeWordListener";

function VoiceAuth() {
  const [text, setText] = useState("");

  const startListening = () => {
    console.log("Wake Word Detected! Starting Voice Recognition...");
    
    // Start speech recognition
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.continuous = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      console.log("User said:", transcript);

      // Send transcript to backend for authentication
      fetch("https://api-gateway-url.amazonaws.com", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      })
        .then((response) => response.json())
        .then((data) => console.log("Server Response:", data));
    };

    recognition.start();
  };

  return (
    <div>
      <WakeWordListener onWakeDetected={startListening} />
      <p>{text}</p>
    </div>
  );
}

export default VoiceAuth;
