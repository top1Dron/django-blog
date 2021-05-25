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

function autocomplete(inp, dict) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("ul");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items list-group w-60");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/

        for ([key, value] of Object.entries(dict)){
            /*check if the item starts with the same letters as the text field value:*/
        
            /*create a DIV element for each matching element:*/
            b = document.createElement("li");
            b.setAttribute("class", "list-group-item w-60");
            /*make the matching letters bold:*/
            if (dict[key].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b.innerHTML = "<strong>" + dict[key].substr(0, val.length) + "</strong>";
                b.innerHTML += dict[key].substr(val.length);
            }
            else {
                b.innerHTML = dict[key].substr(0, val.length) + dict[key].substr(val.length);
            }
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + dict[key] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
            /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                document.location.href = '/blog/' + `${key}`;

                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

function ajax_json_fill_object(type, url, fillingObject){
    var request = new XMLHttpRequest();
    request.open(type, url, true);


    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var resp = JSON.parse(this.response);
            for ([key, value] of Object.entries(resp)){
                fillingObject[key] = value;
            }
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.send();
}

ready(function(){

    var search_post_input = document.getElementById('searchPost');
    search_post_input.addEventListener('input', function(e){
        var search_problem_url = search_post_input.getAttribute('search-posts') + '?search_title=' + search_post_input.value;
        var posts = {};
        ajax_json_fill_object('GET', search_problem_url, posts);
        autocomplete(search_post_input, posts);
    });
    

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
                    errorBlock.innerHTML = '<div class="alert alert-success" role="alert">Successfully log in.</div>';
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
                    errorBlock.innerHTML = '<div class="alert alert-success" role="alert">Successfully sign up and log in.</div>';
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