import { useState } from 'react';
import { Routes, Route } from 'react-router-dom'; // Remove BrowserRouter import
import Home from './pages/Home';
import Login from './pages/Login';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <Routes>
      {/* Define the routes and the components to be rendered */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

export default App;