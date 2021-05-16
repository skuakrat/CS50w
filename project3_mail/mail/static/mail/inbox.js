document.addEventListener('DOMContentLoaded', function load() {
  const useremail = document.querySelector('h2').innerHTML;

  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  load_mailbox('inbox');

  //compose submit
  document.querySelector('#submit').addEventListener('click', function submit() {

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
        user: useremail,
        read: false,
        archived: false,
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
        load_mailbox('sent');
        console.log(result);
        return false;
      }
      
    })
  });

  function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    composeAlert.style.display = 'none';
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    
    
    fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      emails.forEach(email => {

        const container = document.createElement('div');
        container.className = 'container py-1 border';

        const row = document.createElement('a');
          row.className = 'row';
          row.setAttribute('href',"#");
          row.setAttribute('onClick',"return false;");

          
        if (mailbox === 'sent') {
          // Add values for each email
          row.innerHTML = `<div class="col-3"><strong>${email.recipients}</strong></div><div class="col-6">${email.subject}</div><div class="col-3">${email.timestamp}</div>`;
        }else{
          if (email.read) {
            container.style.backgroundColor = 'rgba(242,245,245,0.8)';
          }
          row.innerHTML = `<div class="col-3"><strong>${email.sender}</strong></div><div class="col-6">${email.subject}</div><div class="col-3">${email.timestamp}</div>`;
        }

        row.addEventListener('click', function addRow() {
          email_view(email.id);
        });
        container.append(row);
        document.querySelector('#emails-view').append(container);
      });
    });
  }

  function email_view(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#reply-view').innerHTML = '';

    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      let sender = document.querySelector('#sender');
      let subject = document.querySelector('#subject');
      let timestamp = document.querySelector('#timestamp');
      let body = document.querySelector('#body');
      let buttonid = document.querySelector('#buttonid');

      sender.innerHTML = `<strong>From:</strong>  ${email.sender}`;
      recipients.innerHTML = `<strong>To:</strong>  ${email.recipients}`;
      subject.innerHTML = `<strong>Subject:</strong>  ${email.subject}`;
      timestamp.innerHTML = `<strong>Time:</strong>  ${email.timestamp}`;
      body.innerHTML = email.body.replace(/\n/g,"<br>");

      if (useremail === email.sender) {
        document.querySelector('#reply').style.display = 'none';
        buttonid.innerHTML = ``;
      }else{
          // make read
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
          read: true
          })
        })
        // button [reply]
        document.querySelector('#reply').style.display = 'block';

        // button [archive] or [unarchieve]  
        if (email.archived) {
          buttonid.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="unarchive">Unarchive</button>`;
          document.querySelector('#unarchive').addEventListener('click', function unArchive() {
            fetch(`/emails/${id}`, {
              method: 'PUT',
              body: JSON.stringify({
              archived: false
              })
            });
            location.reload();
          });
        }else{
          buttonid.innerHTML = `<button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>`;
          document.querySelector('#archive').addEventListener('click', function arChive() {
            fetch(`/emails/${id}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived: true
              })
            });
            location.reload();
          });
        }


          //reply function
          document.querySelector('#reply').addEventListener('click', function reply() {

            document.querySelector('#reply').style.display = 'none';
            if(document.getElementById("submitreply")){
              document.getElementById("subjectinput").remove();
              document.getElementById("textarea").remove();
              document.getElementById("submitreply").remove();
            }
            
            let subjectinput = document.createElement('input');
            subjectinput.setAttribute('type',"text");
            subjectinput.setAttribute('id',"subjectinput");
            subjectinput.className = 'form-control';
            resubject = `${email.subject}` ;
            if (resubject.startsWith("Re:")) { subjectinput.value = `${email.subject}`; 
            } else { subjectinput.value = `Re: ${email.subject}`; 
            }
            document.querySelector('#reply-view').append(subjectinput);

            let textarea = document.createElement('textarea');
            textarea.setAttribute('id',"textarea");
            textarea.className = 'form-control';
            textarea.value = `


-------------- ${email.sender}, ${email.timestamp} wrote: --------------
Subject: ${email.subject}

${email.body}`;
            document.querySelector('#reply-view').append(textarea);
      
            //create reply
            let submitreply = document.createElement('button');
            submitreply.className = 'btn btn-sm btn-outline-primary';
            submitreply.setAttribute('id',"submitreply");
            submitreply.innerHTML = 'Send';
            document.querySelector('#reply-view').append(submitreply);          
          
          
            document.querySelector('#submitreply').addEventListener('click', function submitReply() {
              let rebody = document.getElementById("textarea").value;
              let resubject = document.getElementById("subjectinput").value;

              fetch(`/emails`, {
                method: 'POST',
                body: JSON.stringify({
                  recipients: email.sender,
                  subject: resubject,
                  body: rebody,
                  user: useremail,
                  sender: useremail,
                  read: false,
                  archived: false,
                })
              })
              .then(response => response.json())
              .then(result => {        
                  load_mailbox('sent');
                  console.log(result);
                  return false; })
                
            })          
          });

      }
    });
    

  }

});

