import React from 'react';
import {Routes, Route} from 'react-router-dom';
import MainMenu from './MainMenu'
import Posts from './Posts';
import Charities from './Charities';
import Auth from './Auth';


const Home = () => {
    return (
        <div>
            <MainMenu />
            <Routes>
                <Route exact path="/" element={<Posts />} />
                <Route path="/posts" element={<Posts />} />
                <Route path="/charities" element={<Charities />} />
                <Route path="/auth" element={<Auth />} />
            </Routes>
        </div>
    )
}

export default Home;