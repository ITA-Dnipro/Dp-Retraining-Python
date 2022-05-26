import React, { useState, useEffect } from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from "../../axiosApi";
import {Button} from "react-bootstrap";
import {Link} from "react-router-dom";

const EditProfile = () => {
    const [editStatus, setEditStatus] = useState('');
    const [errorMessage, setErrorMessage] = useState('Unknown Error');
    const [editFirstName, setEditFirstName] = useState('');
    const [editLastName, setEditLastName] = useState('');
    const [editUsername, setEditUsername] = useState('');
    const [editEmail, setEditEmail] = useState('');
    const [editPhoneNumber, setEditPhoneNumber] = useState('');
    const onEditEmailChange = (event) => { setEditEmail(event.target.value) }
    const onEditFirstNameChange = (event) => { setEditFirstName(event.target.value) }
    const onEditLastNameChange = (event) => { setEditLastName(event.target.value) }
    const onEditUsernameChange = (event) => { setEditUsername(event.target.value) }
    const onEditPhoneNumberChange = (event) => { setEditPhoneNumber(event.target.value) }

    let editStatusMessage;
    let userId = localStorage.getItem('user_id');

    const alertSuccess = () => {
        return (
            <>
            <Alert key={'success'} variant={'success'}>Changes saved!</Alert>
            <Button as={Link} to="/profile" variant="outline-success">
              Return to Profile
            </Button>
            </>
        )
    }

    const alertFail = () => {
        return (
            <>
            <Alert key={'danger'} variant={'danger'}>{ errorMessage }</Alert>
            <Button as={Link} to="/profile" variant="outline-danger">
              Cancel Changes
            </Button>
            </>
        )
    } 

    if (editStatus === 'success') {
        editStatusMessage = alertSuccess()
    } else if (editStatus === 'fail') {
        editStatusMessage = alertFail()
    }

    useEffect(() => {
        axiosInstance.get(
            `users/${userId}`
        )
            .then(result => {
                setEditFirstName(result.data.data.first_name);
                setEditLastName(result.data.data.last_name);
                setEditEmail(result.data.data.email);
                setEditUsername(result.data.data.username);
                setEditPhoneNumber(result.data.data.phone_number);
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
            'phone_number': editPhoneNumber
        }
        axiosInstance.put(
            `users/${userId}`,
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

                if (error.response.data.detail === undefined) {
                    setErrorMessage(error.response.data.errors[0].detail)
                } else {
                    setErrorMessage(error.response.data.detail[0].msg)
                }
            });
    }

    return (
        <div id="entry-container">
            <div id="entry-wrapper" className="col-lg-4 mx-auto my-4">
                <div className="card border-dark mb-3">
                    <div className="card-header"><h4>Profile Edit</h4></div>
                    <div className="card-body">
                        <form onSubmit={onEditSubmit}>
                            <div className="form-group">
                                <label htmlFor="edit-first-name">First name</label>
                                <input type="text" className="form-control" id="edit-first-name"
                                       name="editFirstName" value={editFirstName}
                                       onChange={onEditFirstNameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="edit-last-name">Last name</label>
                                <input type="text" className="form-control" id="edit-last-name"
                                       name="editLastName" value={editLastName}
                                       onChange={onEditLastNameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="edit-username">Username</label>
                                <input type="text" className="form-control" id="edit-username"
                                       name="editUsername" value={editUsername}
                                       onChange={onEditUsernameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="edit-email">Email</label>
                                <input type="email" className="form-control" id="edit-email" name="editEmail"
                                       value={editEmail} onChange={onEditEmailChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="edit-phone-number">Phone number</label>
                                <input type="text" className="form-control" id="edit-phone-number"
                                       name="editPhoneNumber" value={editPhoneNumber}
                                       onChange={onEditPhoneNumberChange}
                                />
                            </div>
                            <button type="submit" className="btn btn-dark btn-block my-2"
                                id="edit-submit">Save Changes
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
