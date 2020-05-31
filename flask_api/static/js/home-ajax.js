loadDecks();


function serializeForm(form){
    // Create the form data object to be passed to JSON
    formData = new FormData(form);
    formJSON = {}
    formData.forEach(function(value, key){
        formJSON[key] = value;
    });
    // Render the checkbox as true/false values
    for (const checkbox of form.querySelectorAll('input[type=checkbox')) {
        formJSON[checkbox.name] = checkbox.checked;
    }
    console.log(formJSON);
    return JSON.stringify(formJSON);
}

function callBackend(endpoint, method, body, callback){
    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch(endpoint, 
        {   
            method: method,
            headers:  new Headers({
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'X-CSRF-TOKEN': csrf_token,
            }),
            body: body,
            credentials: 'include'
    })
    .then(res => {
        if (!res.ok) {
            throw Error(res.statusText);
        }
        return res;
    })
    .then(res => res.json())
    .then(data => callback(data))
    .catch(reportError);  /* TODO: HANDLE BETTER */
}

function reportError(message) {
    console.log(message);
    alert("An error occured.");
}



function loadDecks(){
    callBackend(
        endpoint='http://127.0.0.1:5000/api/decks',
        method = "GET",
        body = null,
        callback = function(data) {
            // Wait for the page to be loaded
            while (document.readyState === "loading") {};
            getNewDeckAlgorithms();
            initialDecksRendering(data);
        }
    )
}

function createNewDeck() {
    form = document.getElementById("create-deck").getElementsByTagName("form")[0];
    form = serializeForm(form);

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks',
        method = "POST",
        body = form,
        callback = function(data){
            hideNewForm();
            updateDeckData(data);
        }
    )
}

function updateDeck(deck_id) {
    form = document.getElementById(""+deck_id).getElementsByTagName("form")[0];
    form = serializeForm(form)

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deck_id, 
        method = "PUT",
        body = form,
        callback = function(data){
            hideForm(deck_id);
            updateDeckData(data, deck_id);
        }
    )
}

function deleteDeck(deck_id) {
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deck_id, 
        method = 'DELETE',
        body = null,
        callback = function(data){
            hideForm(deck_id);
            updateDeckData(data, deck_id);
        }
    )
}

function getNewDeckAlgorithms(){
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/algorithms',
        method = "GET",
        body = null, 
        callback = renderNewDeckAlgorithms
    )
}
