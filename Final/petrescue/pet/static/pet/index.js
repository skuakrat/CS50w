function fav(post_id) {
    var favButton = document.getElementById(`fav-${post_id}`);
    var unfavButton = document.getElementById(`unfav-${post_id}`);

    fetch(`fav/${post_id}`)
    .then(response => {        
        favButton.style.display = 'none';
        unfavButton.style.display = 'inline';
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });

}


function unfav(post_id) {
    var favButton = document.getElementById(`fav-${post_id}`);
    var unfavButton = document.getElementById(`unfav-${post_id}`);

    fetch(`unfav/${post_id}`)
    .then(response => {        
        favButton.style.display = 'inline';
        unfavButton.style.display = 'none';
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });

}
