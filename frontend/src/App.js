import React from 'react';
import {BrowserRouter} from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Home from './components/Home';


const App = () => {
  return (
    <div className="App">
        <BrowserRouter>
            <Header />
            <Home />
        </BrowserRouter>
    </div>
  );
}

export default App;
