function ready(fn) {
    if (document.readyState != 'loading'){
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};

ready(function(){
    document.getElementById('signinModalForm').addEventListener('submit', function(e){
        e.preventDefault();
        var request = new XMLHttpRequest();
        request.open('POST', document.getElementById('signinModalForm').getAttribute('login_url'), true);
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        var data = {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'username': document.getElementById('id_username').value,
            'password': document.getElementById('id_password').value,
        };

        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                response = JSON.parse(this.response);
                var errorBlock = document.getElementById('signInErrors');
                if (Object.keys(response).length == 0){
                    errorBlock.innerHTML = '';
                    location.reload();
                }
                
                var errorHTML = '';
                for ([key, value] of Object.entries(response)){
                    errorHTML += '<div class="alert alert-danger" role="alert">';
                    errorHTML += `${value}`;
                    errorHTML += '</div>';
                }
                errorBlock.innerHTML = errorHTML;
            }
        };

        request.onerror = function() {
            alert('Something went wrong!');
        };

        request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        data = JSON.stringify(data);
        request.send(data);
    });

    document.getElementById('signUpModalForm').addEventListener('submit', function(e){
        e.preventDefault();
        var request = new XMLHttpRequest();
        request.open('POST', document.getElementById('signUpModalForm').getAttribute('signup_url'), true);
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        var data = {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'username': document.getElementById('id_signup_username').value,
            'email': document.getElementById('id_email').value,
            'password1': document.getElementById('id_password1').value,
            'password2': document.getElementById('id_password2').value,
        };

        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                response = JSON.parse(this.response);
                var errorBlock = document.getElementById('signUpErrors');
                if (Object.keys(response).length == 0){
                    errorBlock.innerHTML = '';
                    location.reload();
                }
                
                var errorHTML = '';
                for ([key, value] of Object.entries(response)){
                    errorHTML += '<div class="alert alert-danger" role="alert">';
                    errorHTML += `${value}`;
                    errorHTML += '</div>';
                }
                errorBlock.innerHTML = errorHTML;
            }
        };

        request.onerror = function() {
            alert('Something went wrong!');
        };

        request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        data = JSON.stringify(data);
        request.send(data);
    });
})