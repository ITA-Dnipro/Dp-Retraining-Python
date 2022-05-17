import React, {useState, useEffect} from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Auth from './components/Auth'
import Posts from './components/Posts';
import Charities from './components/Charities';
import Home from './components/Home';
import Profile from './components/Profile/Profile';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const checkAuthentication = () => {
    const token = localStorage.getItem('access_token');

    setIsAuthenticated(Boolean(token));
  };

  useEffect(() => {
    checkAuthentication();
  }, []);

  return (
    <div className="App">
        <BrowserRouter>
            <Header
              isAuthenticated={isAuthenticated}
              setIsAuthenticated={setIsAuthenticated}
            />
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/home" element={<Home />} />
                <Route path="/posts" element={<Posts />} />
                <Route path="/charities" element={<Charities />} />
                <Route path="/auth" element={<Auth />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/auth" element={<Auth setIsAuthenticated={setIsAuthenticated} />} />
            </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
