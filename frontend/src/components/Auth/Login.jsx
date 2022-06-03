import React, {useState} from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from '../../axiosApi';
import { loginPath } from '../../constants/apiRoutes';

const Login = ({setIsAuthenticated}) => {
    const [loginUsername, setLoginUsername] = useState('');
    const [loginPassword, setLoginPassword] = useState('');

    const onLoginUsernameChange = (event) => { setLoginUsername(event.target.value) }
    const onLoginPasswordChange = (event) => { setLoginPassword(event.target.value) }

    const onLoginSubmit = (event) => {
        event.preventDefault();
        let payload = {
            'username': loginUsername,
            'password': loginPassword,
        }
        console.log(payload);
        axiosInstance.post(
                loginPath,
                payload
            )
            .then(response => {
                const accessToken = response.data.data.access_token;
                const tokenPayload = JSON.parse(atob(accessToken.split('.')[1]));
                const userId = tokenPayload.user_data.id;
                localStorage.setItem('user_id', userId);
                window.location.href = '/';
            })
            .catch(error => {
                setIsAuthenticated(false);
                console.log(error);
            });
    }

    return (
        <div id="login-container">
            <div id="login-wrapper" className="col-lg-4 mx-auto my-4">
                <div className="card border-info mb-3">
                    <div className="card-header">
                        <h4>
                            Login
                        </h4>
                    </div>
                    <div className="card-body">
                        <form onSubmit={onLoginSubmit}>
                            <div className="form-group">
                                <label htmlFor="login-username">
                                    Username
                                </label>
                                <input type="text" className="form-control" id="login-username"
                                       placeholder="Enter username" name="loginUsername"
                                       value={loginUsername} onChange={onLoginUsernameChange}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="login-password">
                                    Password
                                </label>
                                <input type="password" className="form-control" id="login-password"
                                       placeholder="Enter password" name="loginPassword"
                                       value={loginPassword} onChange={onLoginPasswordChange}
                                />
                            </div>
                            <button type="submit" className="btn btn-primary btn-block my-2"
                                    id="login-submit">
                                Submit
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;
