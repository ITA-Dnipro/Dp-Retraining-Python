import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import { Alert, Button } from 'react-bootstrap';
import axiosInstance from "../../axiosApi";
import CharityIcon from './CharityIcon';
import CharityCreationForm from './CharityCreationForm';

const Charities = () => {
    const [charitiesState, setCharitiesState] = useState([]);
    const [isCreationFormVisible, setIsCreationFormVisible] = useState(false);

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
            <div key={id} className="charity-card d-flex flex-row mx-auto my-4 border border-dark rounded">
                <div className="col-4 mx-auto my-2">
                    <CharityIcon width="46" height="46" />
                </div>
                <div className="col-6 mx-auto my-2">
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

    const onCreateButtonClick = (e) => {
        setIsCreationFormVisible(true);
    }

    const onCharityCreated = () => {
        loadCharities();
    }

    return (
        <div>
            <div className="col-4 col-lg-2 mx-auto pt-4">
                <div className={isCreationFormVisible ? "d-none" : ""}>
                    <Button variant="secondary" size="lg" className="w-100 my-2" onClick={onCreateButtonClick}>
                        Create
                    </Button>
                </div>
                <div className={isCreationFormVisible ? "" : "d-none"}>
                    <CharityCreationForm setFormVisibility={setIsCreationFormVisible}
                                         onCharityCreated={onCharityCreated} />
                </div>
                {charityList()}
            </div>
        </div>
    )
}

export default Charities;
