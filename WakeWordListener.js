import React, { useState } from "react";

const WakeWordListener = ({ onWakeDetected }) => {
    const [isListening, setIsListening] = useState(false);

    const startRecording = async () => {
        setIsListening(true);
        console.log("Listening for wake word...");

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const formData = new FormData();
                formData.append("audio", audioBlob, "wakeword.wav");

                console.log("Sending audio to backend for wake word detection...");

                const response = await fetch("http://127.0.0.1:5000/detect_wake_word", {
                    method: "POST",
                    body: formData,
                });

                const data = await response.json();
                console.log("Backend response:", data);

                if (data.wake_word_detected) {
                    console.log("Wake word detected!");
                    onWakeDetected();
                } else {
                    console.log("No wake word detected.");
                }
            };

            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 3000); // Record for 3 seconds
        } catch (error) {
            console.error("Error accessing microphone:", error);
        }
    };

    return (
        <div>
            <p>{isListening ? "Listening..." : "Waiting for wake word..."}</p>
            <button onClick={startRecording}>Start Listening</button>
        </div>
    );
};

export default WakeWordListener;
