import "./Profile.css"

 const Profile = () => {
    return (
        <>
            <div className="profile">
                <div className="profileCenter">
                    <div className="profileCover">
                        <img className="profileUserImg" src="exampleAvatar.jpg" alt="" />
                    </div>
                    <div className="profileInfo">
                        <span className="profileFullName">Jon Snow</span>
                        <span className="profileUsernameValue">kingofthenorth</span>
                        <span className="email">Email: j.snow@nightswatch.com</span>
                        <span className="phone">Phone number: +380661234567</span>
                    </div>
                </div>
            </div>

        </>
    );
}

export default Profile
