import React, {useState, useEffect} from 'react';
import { Alert } from 'react-bootstrap';
import axiosInstance from '../../axiosApi';
import { validateName, validateEmail, validatePhoneNumber} from '../../utils/validators';
import { signupPath } from '../../constants/apiRoutes';

const Signup = () => {
    const [registrationStatus, setRegistrationStatus] = useState('');

    const [isFieldsValidated, setIsFieldsValidated] = useState(false);

    const [signupFields, setSignupFields] = useState({
        firstName: {
            name: 'first_name',
            value: '',
            required: false,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [validateName],
        },
        lastName: {
            name: 'last_name',
            value: '',
            required: false,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [validateName],
        },
        username: {
            name: 'username',
            value: '',
            required: true,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [validateName],
        },
        email: {
            name: 'email',
            value: '',
            required: true,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [validateEmail],
        },
        phoneNumber: {
            name: 'phone_number',
            value: '',
            required: true,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [validatePhoneNumber],
        },
        password: {
            name: 'password',
            value: '',
            required: true,
            blank: false,
            hint: '',
            errors: [],
            validated: false,
            validators:  [],
        },
    });

    useEffect(() => {
        checkFieldsValidation();
    }, [signupFields]);

    const checkFieldsValidation = () => {
        const validated = Object.keys(signupFields).reduce((previous, field) => {
            return (previous && signupFields[field].validated);
        }, true);
        setIsFieldsValidated(validated);
    }

    const setField = (fieldName, newValue) => {
        setSignupFields({...signupFields, [fieldName]: {...signupFields[fieldName], value: newValue}},);
    }

    const getChangeHandler = (fieldName) => {
        return (
            (event) => {setField(fieldName, event.target.value);}
        )
    }

    const checkField = (fieldName) => {
        let errors = [];
        let validated = true;
        if (signupFields[fieldName].required || signupFields[fieldName].value.length > 0) {
            signupFields[fieldName].validators.forEach(validator => {
                let validation = validator(signupFields[fieldName].value);
                errors.push(...validation.errors);
                validated = validated && validation.validated;
            });
        }
        setSignupFields(
            {...signupFields, [fieldName]: {...signupFields[fieldName], errors: errors, validated: validated}}
        );
    }

    const getBlurHandler = (fieldName) => {
        return () => {
            checkField(fieldName);
        };
    }

    const onRegistrationSubmit = (event) => {
        event.preventDefault();
        let payload = {};

        Object.entries(signupFields).forEach(([_, fieldData]) => {
            if (fieldData.value.length > 0 || fieldData.blank) {
                payload[fieldData.name] = fieldData.value;
            }
        });

        axiosInstance.post(
            signupPath,
            payload
        )
            .then(response => {
                console.log('new user registered');
                console.log(response);
                setRegistrationStatus('success');
                window.location.href = '/login';
            })
            .catch(error => {
                console.log('registration failed');
                console.log(error);
                setRegistrationStatus('fail');
            });
    }

    const renderFieldErrors = (fieldName) => {
        let errors = signupFields[fieldName].errors;
        return (
            <div className="text-start text-danger">
                {errors.map((e, idx) => {
                   return (<li key={idx}>{e}</li>)
                 })}
            </div>
        );
    }

    let registrationStatusMessage;

    if (registrationStatus==='success') {
        registrationStatusMessage = <Alert key={'success'} variant={'success'}>Registered!</Alert>
    } else if (registrationStatus==='fail') {
        registrationStatusMessage = <Alert key={'danger'} variant={'danger'}>Registration failed!</Alert>
    }

    return (
        <div id="signup-container">
            <div id="signup-wrapper" className="col-lg-4 mx-auto my-4">
                <div className="card border-warning mb-3">
                    <div className="card-header"><h4>Signup</h4></div>
                    <div className="card-body">
                        <form onSubmit={onRegistrationSubmit}>
                            <div className="form-group">
                                <label htmlFor="register-first-name">
                                    First name
                                </label>
                                <input type="text" className="form-control" id="register-first-name"
                                       placeholder="Enter first name" name="registerFirstUsername"
                                       value={signupFields.firstName.value} onChange={getChangeHandler('firstName')}
                                       onBlur={getBlurHandler('firstName')}
                                />
                                {renderFieldErrors('firstName')}
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-last-name">
                                    Last name
                                </label>
                                <input type="text" className="form-control" id="register-last-name"
                                       placeholder="Enter last name" name="registerLastName"
                                       value={signupFields.lastName.value} onChange={getChangeHandler('lastName')}
                                       onBlur={getBlurHandler('lastName')}
                                />
                                {renderFieldErrors('lastName')}
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-username">
                                    Username
                                </label>
                                <input type="text" className="form-control" id="register-username"
                                       placeholder="Enter username" name="registerUsername"
                                       value={signupFields.username.value} onChange={getChangeHandler('username')}
                                       onBlur={getBlurHandler('username')}
                                />
                                {renderFieldErrors('username')}
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-email">
                                    Email
                                </label>
                                <input type="email" className="form-control" id="register-email"
                                       placeholder="Enter email" name="registerEmail"
                                       value={signupFields.email.value} onChange={getChangeHandler('email')}
                                       onBlur={getBlurHandler('email')}
                                />
                                {renderFieldErrors('email')}
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-phone-number">
                                    Phone number
                                </label>
                                <input type="text" className="form-control" id="register-phone-number"
                                       placeholder="Enter number" name="registerPhoneNumber"
                                       value={signupFields.phoneNumber.value} onChange={getChangeHandler('phoneNumber')}
                                       onBlur={getBlurHandler('phoneNumber')}
                                />
                                {renderFieldErrors('phoneNumber')}
                            </div>
                            <div className="form-group">
                                <label htmlFor="register-password">
                                    Password
                                </label>
                                <input type="password" className="form-control" id="register-password"
                                       placeholder="Enter password" name="registerPassword"
                                       value={signupFields.password.value} onChange={getChangeHandler('password')}
                                       onBlur={getBlurHandler('password')}
                                />
                                {renderFieldErrors('password')}
                            </div>
                            <button type="submit" className="btn btn-warning btn-block my-2"
                                    id="register-submit" disabled={!isFieldsValidated}>
                                Submit
                            </button>
                            {registrationStatusMessage}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Signup;
