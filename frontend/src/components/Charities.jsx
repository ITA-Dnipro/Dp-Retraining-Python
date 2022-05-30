import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import axiosInstance from "../axiosApi";

const Charities = () => {
    const [charitiesState, setCharitiesState] = useState([]);

    useEffect(() => {
        loadCharities();
    }, []);

    const loadCharities = () => {
        axiosInstance.get(
            `charities/`
            )
            .then(response => {
                setCharitiesState(response.data.data);
                console.log(response.data.data);
            })
            .catch(error => {
                console.log(error);
            });
    }

    const charityCard = (id, title, description, phone_number, email) => {
        return (
            <div key={id} className="charity-card d-flex flex-row mx-auto my-4 border border-primary rounded">
                <div className="col-3 mx-auto">
                </div>
                <div className="col-8 mx-auto">
                    <div className="text-left"><h3>{title}</h3></div>
                    <Link to={"/charities/"+id}>Details</Link>
                </div>
            </div>
        );
    }

    const charityList = () => {
        const charityList = charitiesState.map(charity => {
            return charityCard(
                charity.id,
                charity.title,
                charity.description,
                charity.phone_number,
                charity.organisation_email
            );
        });
        return (
            <div className="charity-list">
                {charityList}
            </div>
        );
    }

    return (
        <div>
            <div className="col-lg-4 mx-auto">
                {charityList()}
            </div>
        </div>
    )
}

export default Charities;
