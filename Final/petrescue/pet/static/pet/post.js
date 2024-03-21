document.addEventListener('DOMContentLoaded', function () {
    var deactButton = document.getElementById('deact');
    var actButton = document.getElementById('act');
    var postId = document.getElementById('postId').value;

    if (deactButton) {

        deactButton.addEventListener('click', function () {
            fetch(`deactivate/${postId}`, {
                method: 'GET'
            })
            .then(response => {        
                deactButton.style.display = 'none';
                actButton.style.display = 'block';
                location.reload();
            })
            .catch(error => {
                console.error("Fetch error:", error);
            });
        });
    }

    if (actButton) {
        actButton.addEventListener('click', function () {
            fetch(`activate/${postId}`, {
                method: 'GET'
            })
            .then(response => {     
                    actButton.style.display = 'none';
                    deactButton.style.display = 'block';
                    location.reload();
            })
            .catch(error => {
                console.error("Fetch error:", error);
            });
        })



    }



})