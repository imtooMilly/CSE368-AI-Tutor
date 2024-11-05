import React, { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Simple validation (you can replace this with more complex logic)
    if (!email || !password) {
      setError('Please fill in both fields');
      return;
    }

    setError('');
    alert('Login Successful');
    // Handle the actual login logic here (e.g., API call)
  };

  return (
    <div style={styles.container}>
      <div style={styles.loginCard}>
        <h2 style={styles.title}>Login to Your Account</h2>

        <form onSubmit={handleSubmit}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              style={styles.input}
            />
          </div>

          {error && <p style={styles.error}>{error}</p>}

          <button type="submit" style={styles.button}>Login</button>
        </form>
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#FFF9BF', // Soft yellow background
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '20px',
  },
  loginCard: {
    backgroundColor: '#FFFFFF', // White background for the login card
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    color: '#CB9DF0', // Light purple color for the title
    fontSize: '2rem',
    textAlign: 'center',
    marginBottom: '20px',
  },
  inputGroup: {
    marginBottom: '15px',
  },
  label: {
    color: '#CB9DF0', // Light purple label color
    fontSize: '1rem',
    marginBottom: '8px',
    display: 'block',
  },
  input: {
    width: '100%',
    padding: '10px',
    fontSize: '1rem',
    borderRadius: '5px',
    border: '1px solid #CB9DF0',
    backgroundColor: '#FFF',
    marginBottom: '10px',
  },
  error: {
    color: '#F0C1E1', // Soft pink color for the error message
    fontSize: '0.875rem',
    textAlign: 'center',
    marginBottom: '10px',
  },
  button: {
    width: '100%',
    padding: '12px',
    fontSize: '1.1rem',
    backgroundColor: '#FDDBBB', // Light peach button color
    color: '#333',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  buttonHover: {
    backgroundColor: '#F0C1E1', // Hover effect for the button
  },
};

export default Login;