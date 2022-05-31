import React, {useState} from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from '../../axiosApi';

const CharityCreationForm = ({setFormVisibility, onCharityCreated}) => {
    const [charityTitle, setCharityTitle] = useState('');
    const [charityDescription, setCharityDescription] = useState('');
    const [charityEmail, setCharityEmail] = useState('');
    const [charityPhone, setCharityPhone] = useState('');

    const onCharityTitleChange = (event) => { setCharityTitle(event.target.value) }
    const onCharityDescriptionChange = (event) => { setCharityDescription(event.target.value) }
    const onCharityEmailChange = (event) => { setCharityEmail(event.target.value) }
    const onCharityPhoneChange = (event) => { setCharityPhone(event.target.value) }

    const onCreateSubmit = (event) => {
        event.preventDefault();
        let payload = {
            "title": charityTitle,
            "description": charityDescription,
            "phone_number": charityPhone,
            "organisation_email": charityEmail
        }
        console.log(payload);
        axiosInstance.post(
                '/charities/',
                payload
            )
            .then(response => {
                console.log(response);
                onCharityCreated();
                alert("New charity has been created");
                cancelCharityCreation();
            })
            .catch(error => {
                console.log(error);
            });
    }

    const clearFields = () => {
        setCharityTitle('');
        setCharityDescription('');
        setCharityEmail('');
        setCharityPhone('');
    }

    const cancelCharityCreation = () => {
        clearFields();
        setFormVisibility(false);
    }

    return (
        <div id="charity-form-wrapper" className="mx-auto my-2">
            <div className="card border-dark">
                <div className="card-header">
                    <h3>
                        Create charity
                    </h3>
                </div>
                <div className="card-body">
                    <form onSubmit={onCreateSubmit}>
                        <div className="form-group mt-1">
                            <label htmlFor="charity-title">
                                Title
                            </label>
                            <input type="text" className="form-control" id="charity-title"
                                   placeholder="" name="charityTitle"
                                   value={charityTitle} onChange={onCharityTitleChange}
                            />
                        </div>
                        <div className="form-group mt-1">
                            <label htmlFor="charity-description">
                                Description
                            </label>
                            <input type="text" className="form-control" id="charity-description"
                                   placeholder="" name="charityDescription"
                                   value={charityDescription} onChange={onCharityDescriptionChange}
                            />
                        </div>
                        <div className="form-group mt-1">
                            <label htmlFor="charity-email">
                                Email
                            </label>
                            <input type="text" className="form-control" id="charity-email"
                                   placeholder="" name="charityEmail"
                                   value={charityEmail} onChange={onCharityEmailChange}
                            />
                        </div>
                        <div className="form-group mt-1">
                            <label htmlFor="charity-phone">
                                Phone number
                            </label>
                            <input type="text" className="form-control" id="charity-phone"
                                   placeholder="" name="charityPhone"
                                   value={charityPhone} onChange={onCharityPhoneChange}
                            />
                        </div>
                        <div className="d-flex flex-row justify-content-evenly mt-2">
                            <button type="submit" className="btn btn-primary btn-block my-2"
                                id="charity-submit">
                                Submit
                            </button>
                            <button type="button" className="btn btn-secondary btn-block my-2"
                                id="charity-cancel" onClick={cancelCharityCreation}>
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default CharityCreationForm;
