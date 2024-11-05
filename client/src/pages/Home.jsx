import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate('/login'); // Navigates to the login page
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Welcome to Your AI Tutor</h1>
        <p style={styles.subtitle}>A personalized learning experience powered by AI</p>
      </div>

      <div style={styles.content}>
        <p style={styles.description}>
          With our AI tutor, you can receive personalized guidance and feedback on your learning journey. 
          Whether you're learning coding, mathematics, or any other subject, our intelligent assistant is here 
          to support your growth with tailored content and insights.
        </p>
        <button style={styles.button} onClick={handleNavigate}>
          Start Learning
        </button>
      </div>

      <div style={styles.footer}>
        <p style={styles.footerText}>Ready to begin your educational journey?</p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#FFF9BF', // Soft yellow background
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#333', // Text color
    fontFamily: 'Arial, sans-serif',
    padding: '0 20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
  },
  title: {
    color: '#CB9DF0', // Light purple title
    fontSize: '3rem',
    margin: 0,
  },
  subtitle: {
    color: '#F0C1E1', // Soft pink for the subtitle
    fontSize: '1.5rem',
    margin: '10px 0',
  },
  content: {
    textAlign: 'center',
    maxWidth: '600px',
    marginBottom: '40px',
  },
  description: {
    color: '#333', // Regular dark text for description
    fontSize: '1.2rem',
    marginBottom: '20px',
  },
  button: {
    backgroundColor: '#FDDBBB', // Light peach button
    border: 'none',
    padding: '12px 24px',
    fontSize: '1rem',
    cursor: 'pointer',
    borderRadius: '8px',
    color: '#333', // Text color for button
    transition: 'background-color 0.3s ease',
  },
  buttonHover: {
    backgroundColor: '#F0C1E1', // Soft pink when hovered
  },
  footer: {
    marginTop: '40px',
  },
  footerText: {
    color: '#CB9DF0', // Light purple for footer text
    fontSize: '1rem',
  }
};

export default Home;