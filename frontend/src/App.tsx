import React from "react";
import "./App.css";
import ChatInterface from "./components/ChatInterface";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>My Chatbot App</h1>
      </header>
      <main>
        <ChatInterface />
      </main>
      <footer>
        <p>Simple Chatbot Demo</p>
      </footer>
    </div>
  );
}

export default App;
