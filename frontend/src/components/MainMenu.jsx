import React from 'react';
import {Link} from 'react-router-dom';


const MainMenu = () => {
    return (
        <div>
            <div>
                <Link to="/posts">Posts</Link>
            </div>
            <div>
                <Link to="/charities">Charities</Link>
            </div>
            <div>
                <Link to="/auth">Auth</Link>
            </div>
        </div>
    )
}

export default MainMenu;