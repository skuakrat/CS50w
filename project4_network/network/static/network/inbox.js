document.addEventListener('DOMContentLoaded', function load() {

  if (document.querySelector("#navfollow") != null) {
  document.querySelector("#navfollow").addEventListener('click', function() {load_posts(`following`,1); pagi('following', 1); })
  document.querySelector("#navprofile").addEventListener('click', function() {load_posts(`${user}`,1); profilepage(`${user}`); pagi(`${user}`, 1);})
  }
  
  load_posts('all',1);
  pagi('all', 1);

  //page
  function pagi(type, page) {
    var page = page
    var type = type
    fetch(`page/${type}`)
    .then(response => response.json())
    .then(link => { 

      var text = "";
      for (var pages = 1; pages <= link.plen; pages++) {
        var idpage = "#b"+pages
        text += "<li class='page-item' style='float: left; cursor:pointer;' id='" + (idpage) + "'><span class='page-link'>" + pages + "</span></li>";
        
      }
      document.querySelector('#pagebutton').innerHTML = text;

      var funcs = [];

      function createFunc(i) {
        return function() {
          
          if( i == page) {
            document.getElementById('#b'+i).className = "page-item active";
            document.getElementById('#b'+i).style.cursor = "default";
          } else {
            document.getElementById('#b'+i).addEventListener('click', function() {load_posts(type,i); pagi(type, i); })
          }



        }.call(this);
      }

      for (var i = 1; i <= link.plen; i++) {  
        funcs[i] = createFunc(i);    
      } 


      document.querySelector('#nextbutton').style.display = 'block';
      document.querySelector('#prebutton').style.display = 'block';


      if (page == 1) {
        document.querySelector('#prebutton').style.display = 'none';
      } 
      if (page == link.plen) {
        document.querySelector('#nextbutton').style.display = 'none';
      }

      document.querySelector('#nextbutton').addEventListener('click', function() {load_posts(type,page+1); pagi(type, page+1); })
      document.querySelector('#prebutton').addEventListener('click', function() {load_posts(type,page-1); pagi(type, page-1); })
    
    
    })
  }


  //new post
  document.querySelector('#submit').addEventListener('click', function submit() {

    let ppost = document.querySelector('#compose-body').value;

    fetch(`/posts/`, {
      method: 'POST',
      body: JSON.stringify({
        ppost: ppost,
      })
    })
    .then(response => response.json())
    .then(result => {        
      let composeAlert = document.querySelector('#composeAlert');
      if (result.error) {  
        composeAlert.style.display = 'block';
        composeAlert.className = 'alert alert-danger';
        composeAlert.innerHTML = result.error;
        console.log(result);
        return false;
      } else {
        composeAlert.style.display = 'none';
        console.log(result);
        location.reload();
        return false;
      }
      
    })
  });



  function load_posts(type, page) {
    fetch(`posts/${type}`, {
      method: 'POST',
      body: JSON.stringify({
        page: page,
      })
    })
    .then(response => response.json())
    .then(posts => {

      posts.forEach(post => {

        const container = document.createElement('div');
        container.className = 'card mb-3';
        const row = document.createElement('div');
          row.className = 'card-body';
          row.setAttribute("id", `row${post.id}`);
          //post text
          const posttext = document.createElement('p');
          posttext.setAttribute("id", `posttext${post.id}`);
          posttext.className = 'card-text';
          posttext.innerHTML = `${post.ppost}`;
          row.append(posttext);
          
          //descriptiom line
          row.innerHTML += `
            <p class="card-text"><small class="text-muted"><strong><span style="cursor:pointer;" id="pname${post.id}">${post.puser}</span></strong>, posted on ${post.pdate} (post-id ${post.id})</small></p>`;
            
            
            
            let indiv = document.createElement('div');
            indiv.setAttribute("id", `numlikes${post.id}`);
            indiv.setAttribute("align", "left");
            indiv.innerHTML += `<i class="fas fa-heart" style="cursor:pointer;" id="plikebutton"></i> <span id="old${post.plikesnum}">${post.plikesnum}</span>`;
            indiv.style.display = 'none';


            let indiv2 = document.createElement('div');
            indiv2.setAttribute("id", `numlikes2${post.id}`);
            indiv2.setAttribute("align", "left");
            indiv2.innerHTML += `<i class="far fa-heart" style="cursor:pointer;" id="plikebutton2"></i> <span id="old2${post.plikesnum}">${post.plikesnum}</span>`;
            indiv2.style.display = 'none';
            indiv.className = "text-dark";
            indiv2.className = "text-dark";


            if (post.plikes.includes(user)) {
              indiv.style.display = 'block';
              indiv2.style.display = 'none';
            } else { 
              indiv.style.display = 'none';
              indiv2.style.display = 'block';
            };          

          // Like function
            indiv.addEventListener('click', () => {
              fetch(`unlikes/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  postid: post.id
                })
              })
              .then(response => response.json())
              .then(json => {
                indiv.style.display = 'none';
                indiv2.style.display = 'block';
                oldplike =  document.getElementById(`old${post.plikesnum}`).innerHTML;
                oldlike = parseFloat(oldplike);
                newplikes = (oldlike-1)
                document.querySelector(`#numlikes2${post.id}`).innerHTML = `<i class="far fa-heart" id="plikebutton"></i> <span id="old2${post.plikesnum}">${newplikes}</span>`;
              });
              console.log("remove", post.plikes, post.puser, user);
            })
          
            indiv2.addEventListener('click', () => {
              fetch(`likes/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  postid: post.id
                })
              })
              .then(response => response.json())
              .then(json => {
                indiv2.style.display = 'none';
                indiv.style.display = 'block';
                oldplike =  document.getElementById(`old2${post.plikesnum}`).innerHTML;
                oldlike = parseFloat(oldplike);
                newplikes = (oldlike+1)
                document.querySelector(`#numlikes${post.id}`).innerHTML = `<i class="fas fa-heart" id="plikebutton"></i>  <span id="old${post.plikesnum}">${newplikes}</span>`;
              });
              console.log("add", post.plikes , post.puser, user, post.myplike);
              //location.reload()
            });

          // edit function
          if ( user == post.puser) {
            const editicon = document.createElement('p');
            editicon.setAttribute("id", `edit${post.id}`);
            editicon.setAttribute("align", "left");
            editicon.className = "text-muted";
            editicon.innerHTML = `<small style="cursor:pointer;" class="text-primary">Edit</small>`;
            
              editicon.addEventListener('click', () => {
                document.querySelector( `#posttext${post.id}`).innerHTML = "";
                row.className = "card-body bg-light";
                indiv.className = "text-primary";
                indiv2.className = "text-primary";
                editicon.style.display = 'none';

                let submitedit = document.createElement('button');
                submitedit.className = 'btn btn-sm btn-primary mt-3';
                submitedit.setAttribute('id',`submitedit${post.id}`);
                submitedit.innerHTML = 'Save';
                row.prepend(submitedit);    
                
                let textarea = document.createElement('textarea');
                textarea.setAttribute('id',`textarea${post.id}`);
                textarea.className = 'form-control';
                textarea.value = `${post.ppost}`;
                row.prepend(textarea);

                document.querySelector(`#submitedit${post.id}`).addEventListener('click', function submitedit() {
                  let repost = document.querySelector(`#textarea${post.id}`).value;
                  let hello = `${repost}`;
  
                  fetch(`/edit/${post.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                      ppost: repost,
                    })
                  })
                  .then(response => response.json())
                  .then(result => {        
                      console.log(result);
                      return false; })
                  
                  textarea.style.display = 'none';    
                  document.querySelector( `#submitedit${post.id}`).style.display = 'none';
                  document.querySelector( `#posttext${post.id}`).innerHTML = hello;
                  document.querySelector( `#row${post.id}`).className = "card-body bg-white";
                  document.querySelector( `#edit${post.id}`).style.display = 'block';
                  indiv.className = "text-dark";
                  indiv2.className = "text-dark";

                })
              })
            row.append(editicon);
          }

        row.append(indiv);
        row.append(indiv2);
        container.append(row);
        document.querySelector('#profile-posts-view').append(container);
        document.getElementById(`pname${post.id}`).addEventListener('click', function()  {load_posts(`${post.puser}`,1); profilepage(`${post.puser}`); pagi(`${post.puser}`, 1);})
      });
    })

    user = document.querySelector('#requestuser1').innerHTML;
    document.querySelector('#profile-posts-view').innerHTML = '';
    document.querySelector('#profile-posts-view').style.display = 'block';
    document.querySelector('#requestuser1').style.display = 'none';

    //display
    if (type == 'all') {
      if (user != "AnonymousUser") {
        document.querySelector('#compose-view').style.display = 'block';
      } else {
        document.querySelector('#compose-view').style.display = 'none';
      }
      
      document.querySelector('#profile-user-view').style.display = 'none';
      document.querySelector('#page-title').innerHTML = 'All posts'; 
    }else if

    (type == 'following') {
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#profile-user-view').style.display = 'none';
      document.querySelector('#page-title').innerHTML = 'Following';
    }

    else {
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#profile-user-view').style.display = 'block';
      document.querySelector('#page-title').innerHTML = 'Posts';
      
    }
  }

  


    
  function profilepage(prouser) {
    fetch(`profile/${prouser}`)
      .then(response => response.json())
      .then(profiles => {
        profiles.forEach (profile => {
          document.querySelector('#rfuser').innerHTML = `${profile.fuser}`;
          document.querySelector('#proemail').innerHTML = `${profile.femail}`;
          document.querySelector('#followersnum').innerHTML = `${profile.ffollowersnum}`;
          document.querySelector('#followingsnum').innerHTML = `${profile.ffollowingsnum}`;

          if (profile.ffollowers == '') {
            document.querySelector('#profollowers').innerHTML = "No followers at the moment.";
          } else {
          document.querySelector('#profollowers2').innerHTML = `,${profile.ffollowers}`;
          followerslist = document.querySelector('#profollowers2').innerHTML
          document.querySelector('#profollowers2').style.display = 'none';
          document.querySelector('#profollowers').innerHTML = `${followerslist.substring(1)}`;
          }

          if (profile.ffollowings == '') {
            document.querySelector('#profollowings').innerHTML = "No followings at the moment.";
          } else {
          document.querySelector('#profollowings').innerHTML = `${profile.ffollowings}`;
          }

          //button
          if (profile.fuser == user || user == "AnonymousUser"){
            document.querySelector('#unfollowbutton').style.display = 'none';
            document.querySelector('#followbutton').style.display = 'none';
          } else {
            if (profile.ffollowers.includes(user)) {
              document.querySelector('#unfollowbutton').style.display = 'block';
              document.querySelector('#followbutton').style.display = 'none';
            } else { 
              document.querySelector('#unfollowbutton').style.display = 'none';
              document.querySelector('#followbutton').style.display = 'block';
            }

            followuser = document.querySelector('#rfuser').innerHTML;
          
            document.getElementById('unfollowbutton').addEventListener('click', () => unfollow(`${followuser}`));
            document.getElementById('followbutton').addEventListener('click', () => follow(`${followuser}`));

            
            
          }  
        })
      })
    }



  function unfollow(thisuser) {
    fetch(`unfollows/${thisuser}`, {
      method: 'PUT',
      body: JSON.stringify({
        user: user
      })
    })
    .then(response => response.json())
    .then(json => {
      document.querySelector('#unfollowbutton').style.display = 'none';
      document.querySelector('#followbutton').style.display = 'block';
      currentfnum = document.querySelector('#followersnum').innerHTML;
      pcurrent = parseFloat(currentfnum)
      newfollowersnum = (pcurrent-1)
      document.querySelector('#followersnum').innerHTML = newfollowersnum;
      if ( newfollowersnum == 0 ){
        document.querySelector('#profollowers').innerHTML = "No followers at the moment.";
      }else {
        currentfollows = document.querySelector('#profollowers2').innerHTML;
        newfollowers = currentfollows.replace(`,${user}`, "")
        document.querySelector('#profollowers2').innerHTML = `${newfollowers}`;
        followerslist = document.querySelector('#profollowers2').innerHTML
        document.querySelector('#profollowers').innerHTML = `${followerslist.substring(1)}`;
      }
      console.log();
      return false;
    });

  };

  function follow(hereuser) {
    fetch(`follows/${hereuser}`, {
      method: 'PUT',
      body: JSON.stringify({
        user: user
      })
    })
    .then(response => response.json())
    .then(json => {
      document.querySelector('#unfollowbutton').style.display = 'block';
      document.querySelector('#followbutton').style.display = 'none';
      currentfnum = document.querySelector('#followersnum').innerHTML;
      pcurrent = parseFloat(currentfnum)
      newfollowersnum = (pcurrent+1)
      document.querySelector('#followersnum').innerHTML = newfollowersnum;
      if ( newfollowersnum == 1 ){
        document.querySelector('#profollowers').innerHTML = `,${user}`;
      }else {
        document.querySelector('#profollowers').innerHTML += `,${user}`;
      }
      

      console.log();
    return false;
    });
  }





});
// the end **YAYY**
