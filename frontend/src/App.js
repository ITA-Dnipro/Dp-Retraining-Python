import React, {useState, useEffect} from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import axios from 'axios';
import './App.css';
import Header from './components/Header/Header';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Posts from './components/Posts/Posts';
import Post from './components/Posts/Post';
import Charities from './components/Charity/Charities';
import Home from './components/Home';
import Profile from './components/Profile/Profile';
import Charity from './components/Charity/Charity';
import EditProfile from './components/Profile/EditProfile';
import { apiURL, authMePath } from './constants/apiRoutes';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const checkAuthentication = () => {
    const checkURL = apiURL + authMePath;

    axios.get(checkURL, { withCredentials: true })
      .then(response => {
          localStorage.setItem('user_id', response.data.data.id);
          setIsAuthenticated(true);
      })
      .catch(error => {
          setIsAuthenticated(false);
      });
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
          <Route path="/posts/:postId" element={<Post />} />
          <Route path="/charities" element={<Charities />} />
          <Route path="/charities/:charityId" element={<Charity />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/edit-profile" element={<EditProfile />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
