document.addEventListener('DOMContentLoaded', function() {
    var gotop = document.getElementById('go-top');

    // Initially hide the button on page load
    gotop.style.display = 'none';

    gotop.addEventListener('click', scrollToTop);

    function scrollToTop() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    }

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 0) {
            // Show the button when not at the top
            gotop.style.display = 'inline-block';
        } else {
            // Hide the button when at the top
            gotop.style.display = 'none';
        }
    });

    fetch(`/new`)
    .then(response => response.json())
    .then(data => {
        const newMailCount = data.new_mail;
        if(newMailCount > 0) {

            document.getElementById('new_mail').textContent = `${newMailCount}`;
        } else {

            document.getElementById('new_mail').textContent = "";
        }
    })
    .catch(error => console.error('Error fetching new mail count:', error));
});
        



window.addEventListener('pageshow', function(event) {
    if (event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        window.location.reload();
    }
});
