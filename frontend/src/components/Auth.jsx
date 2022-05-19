import React, {useState, useEffect} from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from "../axiosApi";


const Auth = ({setIsAuthenticated}) => {
    const [registrationStatus, setRegistrationStatus] = useState('');

    const [loginUsername, setLoginUsername] = useState('');
    const [loginPassword, setLoginPassword] = useState('');
    const [registrationUsername, setRegistrationUsername] = useState('');
    const [registrationEmail, setRegistrationEmail] = useState('');
    const [registrationPassword, setRegistrationPassword] = useState('');
    const [registrationPhoneNumber, setRegistrationPhoneNumber] = useState('');

    const onLoginUsernameChange = (event) => { setLoginUsername(event.target.value) }
    const onLoginPasswordChange = (event) => { setLoginPassword(event.target.value) }
    const onRegistrationPasswordChange = (event) => { setRegistrationPassword(event.target.value) }
    const onRegistrationEmailChange = (event) => { setRegistrationEmail(event.target.value) }
    const onRegistrationUsernameChange = (event) => { setRegistrationUsername(event.target.value) }
    const onRegistrationPhoneNumberChange = (event) => { setRegistrationPhoneNumber(event.target.value) }

    let registrationStatusMessage;

    if (registrationStatus==='success') {
        registrationStatusMessage = <Alert key={'success'} variant={'success'}>Registered!</Alert>
    } else if (registrationStatus==='fail') {
        registrationStatusMessage = <Alert key={'danger'} variant={'danger'}>Registration failed!</Alert>
    }

    const onLoginSubmit = (event) => {
        event.preventDefault();
        let payload = {
            'username': loginUsername,
            'password': loginPassword,
        }
        console.log(payload);
        axiosInstance.post(
                '/auth/login/',
                payload
            )
            .then(response => {
                const accessToken = response.data.data.access_token;
                const refreshToken = response.data.data.refresh_token;
                const tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
                const userId = tokenPayload.user_data.id;
                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);
                localStorage.setItem('user_id', userId);
                window.location.href = '/';
            })
            .catch(error => {
                setIsAuthenticated(false);
                console.log(error);
            });
    }

    const onRegistrationSubmit = (event) => {
        event.preventDefault();
        let payload = {
            'username': registrationUsername,
            'email': registrationEmail,
            'password': registrationPassword,
            'phone_number': registrationPhoneNumber,
        }
        axiosInstance.post(
            '/users/',
            payload
        )
            .then(response => {
                console.log('new user registered');
                console.log(response);
                setRegistrationUsername('');
                setRegistrationEmail('');
                setRegistrationPassword('');
                setRegistrationPhoneNumber('');
                setRegistrationStatus('success');
            })
            .catch(error => {
                console.log('registration failed');
                console.log(error);
                setRegistrationStatus('fail');
            });
    }

    return (
        <div id="entry-container">
            <div id="entry-wrapper" className="col-lg-4 mx-auto my-4">
                <div className="card border-info mb-3">
                    <div className="card-header"><h4>Sign In</h4></div>
                    <div className="card-body">
                        <form onSubmit={onLoginSubmit}>
                            <div className="form-group">
                                <label htmlFor="login-username">Username</label>
                                <input type="text" className="form-control" id="login-username"
                                       placeholder="Enter username" name="loginUsername"
                                       value={loginUsername} onChange={onLoginUsernameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="login-password">Password</label>
                                <input type="password" className="form-control" id="login-password"
                                       placeholder="Enter password" name="loginPassword"
                                       value={loginPassword} onChange={onLoginPasswordChange}
                                />
                            </div>
                            <button type="submit" className="btn btn-primary btn-block my-2"
                                    id="login-submit">Submit
                            </button>
                        </form>
                    </div>
                </div>
                <div className="card border-warning mb-3">
                    <div className="card-header"><h4>Register</h4></div>
                    <div className="card-body">
                        <form onSubmit={onRegistrationSubmit}>
                            <div className="form-group">
                                <label htmlFor="register-username">Username</label>
                                <input type="text" className="form-control" id="register-username"
                                       placeholder="Enter username" name="registerUsername"
                                       value={registrationUsername} onChange={onRegistrationUsernameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-email">Email</label>
                                <input type="email" className="form-control" id="register-email"
                                       placeholder="Enter email" name="registerEmail"
                                       value={registrationEmail} onChange={onRegistrationEmailChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-phone-number">Phone number</label>
                                <input type="text" className="form-control" id="register-phone-number"
                                       placeholder="Enter number" name="registerPhoneNumber"
                                       value={registrationPhoneNumber} onChange={onRegistrationPhoneNumberChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-password">Password</label>
                                <input type="password" className="form-control" id="register-password"
                                       placeholder="Enter password" name="registerPassword"
                                       value={registrationPassword} onChange={onRegistrationPasswordChange}
                                />
                            </div>
                            <button type="submit" className="btn btn-warning btn-block my-2"
                                    id="register-submit">Submit
                            </button>
                            {registrationStatusMessage}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Auth;
