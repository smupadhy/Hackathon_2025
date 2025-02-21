import React from "react";
import { useAuth } from "react-oidc-context";
import VoiceAssistant from "./VoiceAssistant";  // NEW LINE added

function App() {
  const auth = useAuth();

  if (auth.isAuthenticated) {
    return (
      <div>
        <h1>Welcome, {auth.user?.profile.email}</h1>
        <VoiceAssistant />  {/* NEW LINE added */}
        <button onClick={() => auth.removeUser()}>Sign out</button>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => auth.signinRedirect()}>Sign in</button>
    </div>
  );
}

export default App;
