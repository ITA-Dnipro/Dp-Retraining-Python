// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage, ref, uploadBytes, getDownloadURL, deleteObject } from "firebase/storage";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "${env:apiKey}", // env variable
    authDomain: "dp-retraining.firebaseapp.com",
    projectId: "dp-retraining",
    storageBucket: "dp-retraining.appspot.com",
    messagingSenderId: "898201285536",
    appId: "1:898201285536:web:6114bcf07dc1a934b76ac5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

// Storage
let userId = localStorage.getItem('user_id');
const storageRef = ref(storage, `UserAvatars/${userId}.png`);

export async function uploadAvatar(file, setLoading, setUserAvatar) {
    console.log(file)

    setLoading(true);
    setUserAvatar("loadingSpinner.svg");

    await uploadBytes(storageRef, file);
    await getDownloadURL(storageRef)
        .then(url => {
            setUserAvatar(url)
        })

    setLoading(false);
}

export async function downloadAvatar(setUserAvatar) {
    await getDownloadURL(storageRef)
        .then(url => {
            setUserAvatar(url)
        })
        .catch(err => {
            console.log(err)
        })
}

export async function deleteAvatar(setUserAvatar) {
    await deleteObject(storageRef)
        .then(() => {
            setUserAvatar('exampleAvatar.jpg')
            console.log("File deleted successfully")
        })
        .catch((err) => {
            console.log(err)
        });
}
