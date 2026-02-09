// src/pages/index.js
import { useState, useEffect } from 'react';
import Head from 'next/head';
import { ChatInterface } from '../components/ChatInterface';

export default function Home() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Decode token to get user info
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
      <Head>
        <title>AI Todo Chatbot</title>
        <meta name="description" content="Manage your todos with AI assistance" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="main">
        <header className="header">
          <h1>AI Todo Chatbot</h1>
          {user && <div className="user-info">Welcome, {user.name || user.email}</div>}
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
          <ChatInterface userId={user.sub || user.userId} />
        )}
      </main>

      <footer className="footer">
        <p>AI-Powered Todo Management System</p>
      </footer>
    </div>
  );
}