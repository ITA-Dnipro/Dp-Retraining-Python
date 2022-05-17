import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Auth from './components/Auth'
import Posts from './components/Posts';
import Charities from './components/Charities';
import Home from './components/Home';

const App = () => {
  return (
    <div className="App">
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/home" element={<Home />} />
                <Route path="/posts" element={<Posts />} />
                <Route path="/charities" element={<Charities />} />
                <Route path="/auth" element={<Auth />} />
            </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
