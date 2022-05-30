import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import axiosInstance from "../../axiosApi";
import "./Charity.css";

const Charity = () => {

    const [charityInfo, setCharityInfo] = useState({});

    const params = useParams();

    useEffect(() => {
        axiosInstance.get(
            `charities/${params.charityId}`
            )
            .then(response => {
                console.log(response);
                setCharityInfo(response.data.data[0]);
            })
            .catch(error => {
                console.log(error);
            });
    }, []);

    return (
        <>
            <div className="charity">
                <div className="charityCenter">
                    <div className="charityCover">
                    </div>
                    <div className="charityInfo">
                        <span className="charityTitle">{charityInfo.title}</span>
                        <span className="charityDescription"><b>Description:</b>{charityInfo.description}</span>
                        <span className="email"><b>Email:</b>{charityInfo.organisation_email}</span>
                        <span className="phone"><b>Phone number:</b>{charityInfo.phone_number}</span>
                    </div>
                </div>
            </div>

        </>
    );
}

export default Charity;
