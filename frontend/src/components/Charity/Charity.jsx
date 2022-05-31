import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import axiosInstance from "../../axiosApi";
import CharityIcon from './CharityIcon';
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
                <div className="col-4">
                    <div className="charityCover">
                    </div>
                    <div className="charityInfo">

                        <div className="d-flex flex-row w-100 mt-2 mb-3">
                            <div className="col-4 text-end me-2">
                                <CharityIcon width="46" height="46" />
                            </div>
                            <div className="col-7 mt-auto">
                                <h1>{charityInfo.title}</h1>
                            </div>
                        </div>

                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-1">
                                <b>Description:{' '}</b>
                            </div>
                            <div className="col-7">
                                {charityInfo.description}
                            </div>
                        </div>
                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-1">
                                <b>Email:{' '}</b>
                            </div>
                            <div className="col-7">
                                {charityInfo.organisation_email}
                            </div>
                        </div>
                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-1">
                                <b>Phone number:{' '}</b>
                            </div>
                            <div className="col-7">
                                {charityInfo.phone_number}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </>
    );
}

export default Charity;
