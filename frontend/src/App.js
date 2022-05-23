import React, {useState, useEffect} from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';
import Header from './components/Header/Header';
import Auth from './components/Auth'
import Posts from './components/Posts';
import Charities from './components/Charities';
import Home from './components/Home';
import Profile from './components/Profile/Profile';
import Charity from './components/Charity/Charity';
import EditProfile from './components/Profile/EditProfile';

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
          <Route path="/charity" element={<Charity />} />
          <Route path="/auth" element={<Auth setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/edit-profile" element={<EditProfile />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
