import React, { useState, useEffect } from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from "../../axiosApi";


const EditProfile = () => {

    const [userInfo, setUserInfo] = useState('');
    const [editStatus, setEditStatus] = useState('');
    const [editFirstName, setEditFirstName] = useState('');
    const [editLastName, setEditLastName] = useState('');
    const [editUsername, setEditUsername] = useState('');
    const [editEmail, setEditEmail] = useState('');
    const [editPassword, setEditPassword] = useState('');
    const [editPhoneNumber, setEditPhoneNumber] = useState('');
    const onEditEmailChange = (event) => { setEditEmail(event.target.value) }
    const onEditFirstNameChange = (event) => { setEditFirstName(event.target.value) }
    const onEditLastNameChange = (event) => { setEditLastName(event.target.value) }
    const onEditUsernameChange = (event) => { setEditUsername(event.target.value) }
    const onEditPhoneNumberChange = (event) => { setEditPhoneNumber(event.target.value) }

    let editStatusMessage;

    if (editStatus === 'success') {
        editStatusMessage = <Alert key={'success'} variant={'success'}>Profile is edited!</Alert>
    } else if (editStatus === 'fail') {
        editStatusMessage = <Alert key={'danger'} variant={'danger'}>Edit failed!</Alert>
    }

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

    const onEditSubmit = (event) => {
        event.preventDefault();
        let payload = {
            'first_name': editFirstName,
            'last_name': editLastName,
            'username': editUsername,
            'email': editEmail,
            'password': editPassword,
            'phone_number': editPhoneNumber,
        }
        axiosInstance.put(
            `users/${userInfo.id}`,
            payload
        )
            .then(response => {
                console.log('user data edited');
                console.log(response);
                setEditStatus('success');
            })
            .catch(error => {
                console.log('Edit failed');
                console.log(error);
                setEditStatus('fail');
            });
    }

    return (
        <div id="entry-container">
            <div id="entry-wrapper" className="col-lg-4 mx-auto my-4">
                <div className="card border-warning mb-3">
                    <div className="card-header"><h4>Profile Edit</h4></div>
                    <div className="card-body">
                        <form onSubmit={onEditSubmit}>
                            <div className="form-group">
                                <label htmlFor="register-first-name">First name</label>
                                <input type="text" className="form-control" id="register-first-name"
                                    placeholder="Enter First Name" name="registerFirstName"
                                    value={editFirstName} onChange={onEditFirstNameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-last-name">Last name</label>
                                <input type="text" className="form-control" id="register-last-name"
                                    placeholder="Enter Last Name" name="registerLastName"
                                    value={editLastName} onChange={onEditLastNameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-username">Username</label>
                                <input type="text" className="form-control" id="register-username"
                                    placeholder="Enter username" name="registerUsername"
                                    value={editUsername} onChange={onEditUsernameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-email">Email</label>
                                <input type="email" className="form-control" id="register-email"
                                    placeholder="Enter email" name="registerEmail"
                                    value={editEmail} onChange={onEditEmailChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-phone-number">Phone number</label>
                                <input type="text" className="form-control" id="register-phone-number"
                                    placeholder="Enter number" name="registerPhoneNumber"
                                    value={editPhoneNumber} onChange={onEditPhoneNumberChange}
                                />
                            </div>
                            <button type="submit" className="btn btn-warning btn-block my-2"
                                id="register-submit">Save Changes
                            </button>
                            {editStatusMessage}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default EditProfile;
