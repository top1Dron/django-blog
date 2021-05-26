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

ready(function(e){
    editButtons = document.querySelectorAll('.edit-comment');
    for (const button of editButtons) {
        button.addEventListener('click', function(e){
            e.preventDefault();
            var request = new XMLHttpRequest();
            request.open('GET', button.getAttribute('load-edit-comment-form-url'), true);

            request.onload = function() {
                if (this.status >= 200 && this.status < 400) {
                    const resp = JSON.parse(this.response);
                    document.getElementById('editCommentModalWrapper').innerHTML = resp['modal-form'];
                    setTimeout(() => {
                        var commentEditForm = document.getElementById('editCommentModal');
                        var myModal = new bootstrap.Modal(commentEditForm, {})
                        console.log(commentEditForm);
                        console.log(myModal);
                        myModal.show();
                    }, 100);
                    // var modal = bootstrap.Modal.getInstance(myModalEl);
                }
            };
        
            request.onerror = function() {
                alert('Something went wrong!');
            };
        
            request.send();
           
        })
    }
})