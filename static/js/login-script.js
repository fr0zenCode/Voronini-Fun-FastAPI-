document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('loginForm');
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    form.addEventListener('submit', function(event){
        event.preventDefault();
        if(checkInputs()){
            sendCredentialsToBackend(email.value, password.value);
        }
    });

    email.addEventListener('input', () =>{
        validateField(email, isEmail(email.value.trim()), 'Некорректный адрес электронной почты');
    });

    // Связь с FastAPI
    async function sendCredentialsToBackend(email, password){
        const response = await fetch("/user/authorize-user", {
            method: "POST",
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        if(response.ok){
            document.location.href = '/user/me'
        }else{

    
            const passwordInput = document.getElementById("password");
            const passwordFormControl = passwordInput.parentElement;
            const passwordIcon = passwordFormControl.querySelector('.icon');
            passwordFormControl.className = 'form-control error';
            passwordIcon.className = 'icon fas fa-times-circle';
        
            // Окрасить поля в красный и написать неверный логин неверный пароль
        }
        
    }

    function checkInputs(){
        let isValid = true;
        validateField(email, isEmail(email.value.trim()), 'Некорректный адрес электронной почты');

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

});

function redirectToRegistrationPage(){
    console.log("Делаю редирект");
    document.location.href = "registration"
}