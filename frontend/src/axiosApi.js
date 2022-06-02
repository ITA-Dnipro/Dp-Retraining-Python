import axios from 'axios'
import { apiURL, refreshPath, logoutPath } from './constants/apiRoutes'

const loginRoute = '/login/'
const badSignatureMessage = 'Your signature are wrong or expired. Please log-in again';

const expirationErrorResponseMessage = 'Signature has expired'

const axiosInstance = axios.create({
    baseURL: apiURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
    },
    credentials: "same-origin",
});

axiosInstance.defaults.withCredentials = true;

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        console.log(error);
        const originalRequest = error.config;
        const originalUrl = originalRequest.url;

        if (
            error.response.status === 422
            && originalUrl === refreshPath
            || error.response.status === 401
        ) {
            if (originalUrl === logoutPath) {
                window.location.href = '/';
            }
            let proceedToLogin = window.confirm(badSignatureMessage);
            if (proceedToLogin) {
                window.location.href = loginRoute;
            }
            return Promise.reject(error);
        }

        if (
            error.response.status === 422
            && error.response.data.errors?.find(e => e.detail === expirationErrorResponseMessage)
        ) {
            return axiosInstance
            .post(refreshPath)
            .then((response) => {
                return axiosInstance(originalRequest);
            })
            .catch(err => {
                return Promise.reject(error);
            });
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;