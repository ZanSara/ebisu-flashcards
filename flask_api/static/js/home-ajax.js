loadDecks();


function loadDecks(){
    // I should have a CSRF token set after logging in
    var token = getCookie("csrf_access_token");

    // Fetch decks data
    fetch('http://127.0.0.1:5000/api/decks', 
        {   
            method:'GET',
            headers:  new Headers({'Authorization': 'Bearer '+token}),
        })
    .then(res => res.json())
    .then((data) => {
        while (document.readyState === "loading") {};
        renderDecks(data);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
}



function saveDeck(deck_id) {
    console.log("IMPLEMENT");
}



function deleteDeck(deck_id) {
    console.log("IMPLEMENT");
}
