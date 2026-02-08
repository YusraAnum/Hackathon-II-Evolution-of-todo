import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ChatInterface } from './components/ChatInterface';
import './App.css';

// Import the components/pages
const Home = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const decoded = JSON.parse(atob(token.split('.')[1]));
        setUser(decoded);
      } catch (error) {
        console.error('Error decoding token:', error);
      }
    }
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <main className="main">
        <header className="header">
          <h1>AI Todo Chatbot</h1>
          {user && <div className="user-info">Welcome, {user.username || user.name || user.email}</div>}
        </header>

        {!user ? (
          <div className="auth-section">
            <button onClick={() => window.location.href = '/login'}>
              Login to Continue
            </button>
            <button onClick={() => window.location.href = '/signup'}>
              Sign Up
            </button>
          </div>
        ) : (
          <div className="dashboard">
            <h2>Your Todo Dashboard</h2>
            <p>You are logged in as: {user.username || user.name || user.email}</p>
            <button
              onClick={() => {
                localStorage.removeItem('auth_token');
                window.location.reload();
              }}
            >
              Logout
            </button>
            <div className="chat-section">
              <h3>AI Assistant</h3>
              <ChatInterface userId={user.sub || user.userId || user.id} />
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>AI-Powered Todo Management System</p>
      </footer>
    </div>
  );
};

// Import the pages
import Signup from './pages/Signup';
import Login from './pages/Login';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;