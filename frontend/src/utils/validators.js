const validateByRegex = (string, pattern) => {
    const re = new RegExp(pattern);
    return re.test(string);
}

export const validateName = (name) => {
    let errors = []
    let validated = true;
    if (name.length < 2 || name.length > 64){
        validated = false;
        errors.push('2-64 characters required');
    }
    return { validated, errors };
}

export const validateEmail = (email) => {
    let errors = []
    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let validated = email.match(re) ? true: false;
    if (!validated) {
        errors.push('Wrong email format');
    }
    return { validated, errors };
}

export const validatePhoneNumber = (phoneNumber) => {
    let errors = []
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
    let validated = phoneNumber.match(re) ? true: false;
    if (!validated) {
        errors.push('Wrong phone number format');
    }
    return { validated, errors};
}