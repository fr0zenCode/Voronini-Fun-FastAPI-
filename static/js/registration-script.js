document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('registrationForm');
    const firstName = document.getElementById('first-name');
    const lastName = document.getElementById('last-name');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const passwordConfirm = document.getElementById('password-confirm');

    form.addEventListener('submit', function(event){
        event.preventDefault();
        if(checkInputs()){
            registrateUser(firstName.value, lastName.value, username.value, email.value, password.value);
        }
    });

    firstName.addEventListener('input', () =>{
        validateField(firstName, firstName.value.trim() !== '', 'Введите ваше имя');
    });

    lastName.addEventListener('input', () =>{
        validateField(lastName, lastName.value.trim() !== '', 'Введите вашу фамилию');
    });

    username.addEventListener('input', () =>{
        validateField(username, username.value.trim() !== '', 'Придумайте никнейм');
    });

    email.addEventListener('input', () =>{
        validateField(email, isEmail(email.value.trim()), 'Введите корректный адрес электронной почты');
    });

    password.addEventListener('input', () =>{
        validateField(password, password.value.trim().length >= 7, 'Пароль должен содержать не менее 7 символов');
    });

    passwordConfirm.addEventListener('input', () =>{
        validateField(passwordConfirm, isPasswordConfirmed(password.value, passwordConfirm.value), 'Пароли не совпадают');
    });

    function checkInputs(){
        let isValid = true;
        validateField(firstName, firstName.value.trim() !== '', 'Введите ваше имя');
        validateField(lastName, lastName.value.trim() !== '', 'Введите вашу фамилию');
        validateField(username, username.value.trim() !== '', 'Придумайте никнейм');
        validateField(email, isEmail(email.value.trim()), 'Введите корректный адрес электронной почты');
        validateField(password, password.value.trim().length >= 7, 'Пароль должен содержать не менее 7 символов');
        if(!validateField(password, password.value.trim().length >= 7, 'Пароль должен содержать не менее 7 символов')){
            passwordConfirm.placeholder = "Сначала придумайте пароль";
        }else{
            validateField(passwordConfirm, isPasswordConfirmed(password.value, passwordConfirm.value), 'Пароли не совпадают');
        }

        document.querySelectorAll('.form-control').forEach((control) =>{
            if(control.classList.contains('error')){
                isValid = false;
            }
        });

        return isValid;

    }

    function validateField(input, condition, errorMessage){
        if(condition){
            setSuccess(input);
        }else{
            SetError(input, errorMessage);
        }
    }

    function SetError(input, message){
        const formControl = input.parentElement;
        const icon = formControl.querySelector('.icon');
        formControl.className = 'form-control error';
        icon.className = 'icon fas fa-times-circle';
        input.placeholder = message;
    }

    function setSuccess(input){
        const formControl = input.parentElement;
        const icon = formControl.querySelector('.icon');
        formControl.className = 'form-control success';
        icon.className = 'icon fas fa-check-circle';
    }

    function isEmail(email){
        return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(email);
    }

    function isPasswordConfirmed(originalPassword, passwordForConformation){
        if(originalPassword == passwordForConformation && originalPassword !== ""){
            return true;
        }else{
            return false;
        }
    }

});

function backToLoginPage(){
    document.location.href = "login";
}

async function registrateUser(firstName, lastName, username, email, password){

    const response = await fetch("/user/registrate-user", {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        body: JSON.stringify({
            first_name: firstName,
            second_name: lastName,
            username: username,
            email: email,
            password: password
        })
    })

    if(response.ok){
        document.location.href = "login";
    }else{
        const json = await response.json();
        const res = JSON.parse(json);
        const errorField = document.getElementById(res.detail);
        const formControl = errorField.parentElement;
        const icon = formControl.querySelector('.icon');
        
        formControl.className = 'form-control error';
        icon.className = 'icon fas fa-times-circle';
        errorField.placeholder = "Такой уже есть";
        
    }
    
}