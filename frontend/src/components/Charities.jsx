import React, { useState, useEffect } from 'react';

const Charities = () => {
    const [charitiesState, setCharitiesState] = useState([
        {
            "id": "c12",
            "title": "Charity 1",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "phone_number": "+380394675559",
            "organisation_email": "c1@mail.com"
        },
        {
            "id": "c2",
            "title": "Charity 2",
            "description": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "phone_number": "+380394679999",
            "organisation_email": "c2@mail.com"
        },
        {
            "id": "c3",
            "title": "Charity 3",
            "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "phone_number": "+380394678888",
            "organisation_email": "c3@mail.com"
        },
        {
            "id": "c4",
            "title": "Charity 4",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "phone_number": "+380394678888",
            "organisation_email": "c4@mail.com"
        }
    ]);

    useEffect(() => {
        loadCharities();
    }, []);

    const loadCharities = () => {
    }

    const charityCard = (id, title, description, phone_number, email) => {
        return (
            <div key={id} className="charity-card mx-auto my-4 border border-primary rounded">
                <div>{id}</div>
                <div>{title}</div>
                <div>{description}</div>
                <div>{phone_number}</div>
                <div>{email}</div>
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
