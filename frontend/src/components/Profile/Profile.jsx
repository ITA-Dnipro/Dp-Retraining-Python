import React, {useEffect, useState} from 'react';
import axiosInstance from "../../axiosApi";
import "./Profile.css";
import {Button} from "react-bootstrap";
import {Link} from "react-router-dom";

 const Profile = () => {
    const [userInfo, setUserInfo] = useState('');

    useEffect(() => {
        let userId = localStorage.getItem('user_id');
        axiosInstance.get(
            `users/${userId}`
            )
            .then(result => {
                setUserInfo(result.data.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <>
            <div className="profile">
                <div className="profileCenter">
                    <div className="profileCover">
                        <img className="profileUserImg" src="exampleAvatar.jpg" alt="" />
                    </div>
                    <div className="profileInfo">
                        <span className="profileFullName">{userInfo.first_name} {userInfo.last_name}</span>
                        <span className="profileUsernameValue">{userInfo.username}</span>
                        <span className="email">Email: {userInfo.email}</span>
                        <span className="phone">Phone number: {userInfo.phone_number}</span>
                        <Button as={Link} to="/edit-profile" variant="outline-dark" className="me-2" >
                         Edit Profile
                        </Button>
                    </div>
                </div>
            </div>

        </>
    );
}

export default Profile;
