loadDecks();


function loadDecks(){
    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch('http://127.0.0.1:5000/api/decks', 
        {   
            method:'GET',
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token
            }),
        })
    .then(res => res.json())
    .then((data) => {
        while (document.readyState === "loading") {};
        renderDecks(data);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
}


function createNewDeck() {
    
    // Create the form data object to be passed to JSON
    formData = new FormData(document.getElementById("create-deck").getElementsByTagName("form")[0]);
    formJSON = {}
    formData.forEach(function(value, key){
        formJSON[key] = value;
    });

    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch('http://127.0.0.1:5000/api/decks', 
        {   
            method:'POST',
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token,
            }),
            body: JSON.stringify(formJSON),
            credentials: 'include'
        })
    .then(res => res.json())
    .then((data) => {
        hideNewForm();
        updateDeckData(data);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
}


function updateDeck(deck_id) {
    
    // Create the form data object to be passed to JSON
    formData = new FormData(document.getElementById(""+deck_id).getElementsByTagName("form")[0]);
    formJSON = {}
    formData.forEach(function(value, key){
        formJSON[key] = value;
    });

    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch('http://127.0.0.1:5000/api/decks/'+deck_id, 
        {   
            method:'PUT',
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token,
            }),
            body: JSON.stringify(formJSON),
            credentials: 'include'
        })
    .then(res => res.json())
    .then((data) => {
        hideForm(deck_id);
        console.log(data);
        updateDeckData(data, deck_id);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
}


function deleteDeck(deck_id) {
    
    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch('http://127.0.0.1:5000/api/decks/'+deck_id, 
        {   
            method:'DELETE',
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token,
            }),
            credentials: 'include'
        })
    .then(res => res.json())
    .then((data) => {
        hideForm(deck_id);
        updateDeckData(data, deck_id);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
}