import logo from './logo.svg';
import './App.css';
import RegisterForm from './register';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import BlogForm from './blogpost';
import LoginForm from './login'
import CategoryForm from './category';

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsLoggedIn(!!token);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
        window.location.href = '/api/login';
    }; 
  return (
    <div className="App">
      <BrowserRouter>
            {/* <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} /> */}
            <Routes>
                {/* <Route path="/api/blog-form" element={isLoggedIn ? <AnusuchiForm /> : <Navigate to="/api/login" />} /> */}
                <Route path="/api/register" element={<RegisterForm />} />
                <Route path="/api/login" element={<LoginForm />} />
                <Route path="/api/blogpost" element={<BlogForm />} />
                <Route path="/api/categories" element={<CategoryForm />} />

                
                {/* <Route path="/api/login" element={ isLoggedIn ? <Navigate to="/api/dashboard" /> : <LoginForm setIsLoggedIn={setIsLoggedIn} />} />
                <Route path="api/dashboard" element={isLoggedIn ? <Dashboard /> : <Navigate to="/api/login" />} /> 
                <Route path="/" element={isLoggedIn ? <Navigate to="api/dashboard" /> : <Navigate to="/api/login" />} />  */}
            </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
