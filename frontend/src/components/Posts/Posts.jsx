import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import PostIcon from './PostIcon';

const Posts = () => {
    const [postsState, setPostsState] = useState([
        {
            "id": "abc12301",
            "title": "Post 1",
            "description": "Description of post 1",
            "goal": 100,
            "balance": 40
        },
        {
            "id": "abc12302",
            "title": "Post 2",
            "description": "Description of post 2",
            "goal": 100,
            "balance": 20
        },
        {
            "id": "abc12303",
            "title": "Post 3",
            "description": "Description of post 3",
            "goal": 100,
            "balance": 70
        },
        {
            "id": "abc12304",
            "title": "Post 4",
            "description": "Description of post 4",
            "goal": 100,
            "balance": 10
        },
        {
            "id": "abc12305",
            "title": "Post 5",
            "description": "Description of post 5",
            "goal": 100,
            "balance": 90
        },
    ]);

    useEffect(() => {
        loadCharities();
    }, []);

    const loadCharities = () => {

    }

    const postCard = (id, title, description) => {
        return (
            <div key={id} className="charity-card d-flex flex-row mx-auto my-4 border border-dark rounded">
                <div className="col-4 mx-auto mb-2 mt-3">
                    <PostIcon width="46" height="46" />
                </div>
                <div className="col-6 mx-auto my-2">
                    <div className="text-left"><h3>{title}</h3></div>
                    <Link to={"/posts/"+id}>Details</Link>
                </div>
            </div>
        );
    }

    const postsList = () => {
        const postsCards = postsState.map(post => {
            return postCard(
                post.id,
                post.title,
                post.description,
            );
        });
        return (
            <div className="charity-list">
                {postsCards}
            </div>
        );
    }


    return (
        <div>
            <div className="col-4 col-lg-2 mx-auto pt-4">
                {postsList()}
            </div>
        </div>
    )
}

export default Posts;
