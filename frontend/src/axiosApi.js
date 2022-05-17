import axios from 'axios'

const baseURL = 'http://localhost:4500/api/v1/';

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Authorization': localStorage.getItem('access_token') ? "JWT " + localStorage.getItem('access_token') : null,
        'Content-Type': 'application/json',
        'accept': 'application/json',
    },
    credentials: "same-origin",
});

axiosInstance.defaults.withCredentials = true;

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        const originalRequest = error.config;

        if (error.response.status === 401 && originalRequest.url === baseURL+'auth/refresh/') {
            window.location.href = '/auth/';
            return Promise.reject(error);
        }

        if (error.response.data.code === "token_not_valid" &&
            error.response.status === 401 &&
            error.response.statusText === "Unauthorized")
            {
                const localRefreshToken = localStorage.getItem('refresh_token');

                if (localRefreshToken){
                    const tokenPayload = JSON.parse(atob(localRefreshToken.split('.')[1]));

                    const now = Math.ceil(Date.now() / 1000);
                    console.log(tokenPayload.exp);

                    if (tokenPayload.exp > now) {
                        return axiosInstance
                        .post('/auth/refresh/', {refresh: localRefreshToken})
                        .then((response) => {
                            const responseAccessToken = response.data.data.access_token;
                            const responseRefreshToken = response.data.data.refresh_token;
                            localStorage.setItem('access_token', responseAccessToken);
                            localStorage.setItem('refresh_token', responseRefreshToken);
//                            axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
//                            originalRequest.headers['Authorization'] = "JWT " + response.data.access;
//                            let cookie = `access_token_cookie=${responseAccessToken}; refresh_token_cookie=${responseRefreshToken}`;
//                            axiosInstance.defaults.headers['Cookie'] = cookie;
//                            originalRequest.headers['Cookie'] = cookie;
                            return axiosInstance(originalRequest);
                        })
                        .catch(err => {
                            console.log(err)
                        });
                    }else{
                        console.log("Refresh token is expired", tokenPayload.exp, now);
                        window.location.href = '/auth/';
                    }
                }else{
                    console.log("Refresh token not available.");
                    window.location.href = '/auth/';
                }
        }

      return Promise.reject(error);
  }
);

export default axiosInstance;