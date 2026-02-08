// src/pages/login.js
import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        // Store the token in localStorage
        localStorage.setItem('auth_token', data.access_token);
        
        // Redirect to home page
        router.push('/');
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <Head>
        <title>Login - AI Todo Chatbot</title>
        <meta name="description" content="Log in to your AI Todo Chatbot account" />
      </Head>

      <main className="main">
        <div className="auth-form">
          <h1>Log In</h1>
          
          {error && <div className="error-message">{error}</div>}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Logging in...' : 'Log In'}
            </button>
          </form>
          
          <div className="auth-links">
            <p>
              Don't have an account?{' '}
              <Link href="/signup">Sign up</Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}