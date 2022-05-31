import React, { useEffect, useState } from 'react';
import axiosInstance from "../../axiosApi";
import "./Profile.css";
import { Button, Form, ButtonGroup, Alert } from "react-bootstrap";
import { Link } from "react-router-dom";
import { uploadAvatar, downloadAvatar, deleteAvatar } from '../../utils/firebase';

const Profile = () => {
    const [userInfo, setUserInfo] = useState('');
    const [showAvatarFail, setShowAvatarFail] = useState(false);
    const [userAvatar, setUserAvatar] = useState("exampleAvatar.jpg");
    const [photo, setPhoto] = useState(null);
    const [loading, setLoading] = useState(false);
    const [displayAvatarEdit, setDisplayAvatarEdit] = useState(false);
    const [displayStyle, setDisplayStyle] = useState("none")

    const userId = localStorage.getItem('user_id');

    useEffect(() => {
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

    const alertAvatarFail = () => {
        if (showAvatarFail) {
            return (
                <>
                    <div className=" d-flex justify-content-center">
                        <Alert className="col-4 my-2" variant={'danger'} onClose={() => setShowAvatarFail(false)} dismissible>
                            <p>
                                Please use image format (jpg, png, svg etc) and make sure that image size is less than 5 mb.
                            </p>
                        </Alert>
                    </div>
                </>
            )
        }

    }

    downloadAvatar(setUserAvatar)

    function handleChange(e) {
        if (e.target.files[0]) {
            setPhoto(e.target.files[0])
        }
    }

    function handleClick() {
        const fileType = photo.type.split("/")[0]
        const fileSize = photo.size

        if (fileType === "image" && fileSize <= 5000000) {
            uploadAvatar(photo, setLoading, setUserAvatar);
            setShowAvatarFail(false);
        } else {
            setShowAvatarFail(true);
        }
    }

    function deleteClick() {
        deleteAvatar(setUserAvatar);
    }

    function showAvatarForm() {
        if (displayAvatarEdit) {
            setDisplayAvatarEdit(false);
            setDisplayStyle("none");
        } else {
            setDisplayAvatarEdit(true);
            setDisplayStyle("flex");
        }
    }

    return (
        <>
            <div className="profile">
                <div className="profileCenter">
                    <div className="profileCover" >
                        <div className="userImg" onClick={showAvatarForm} >
                            <img className="profileUserImg" src={userAvatar} alt="Avatar" />
                            <div class="editAvatar">
                                <img className="editAvatarImg" src="editAvatar.png" alt="Edit Avatar" />
                            </div>
                        </div>
                    </div>
                    <div className="avatarForm" style={{ display: displayStyle }}>
                        <Form>
                            <Form.Control type="file" size="sm" onChange={handleChange} className="my-2 avatarEdit" />
                            <ButtonGroup size="sm">
                                <Button variant="outline-dark" size="sm" disabled={!photo || loading} onClick={handleClick}>Upload avatar</Button>
                                <Button variant="outline-danger" size="sm" disabled={userAvatar === 'exampleAvatar.jpg'} onClick={deleteClick}>Delete avatar</Button>
                            </ButtonGroup>
                        </Form>
                    </div>
                    {alertAvatarFail()}
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
