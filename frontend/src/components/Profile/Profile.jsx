import React, {useEffect, useState} from 'react';
import axiosInstance from "../../axiosApi";
import "./Profile.css";

 const Profile = () => {
    const [userInfo, setUserInfo] = useState('');

    useEffect(() => {
        let userId = localStorage.getItem('user_id');
        axiosInstance.get(
            `users/${userId}`
            )
            .then(response => response)
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
                    </div>
                </div>
            </div>

        </>
    );
}

export default Profile;
