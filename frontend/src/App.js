import React from 'react';
import {BrowserRouter} from 'react-router-dom';
import './App.css';
import Header from './components/Navbar';
import Profile from './components/Profile/Profile';

const App = () => {
  return (
    <div className="App">
        <BrowserRouter>
            <Header />
            <Profile />
        </BrowserRouter>
    </div>
  );
}

export default App;
