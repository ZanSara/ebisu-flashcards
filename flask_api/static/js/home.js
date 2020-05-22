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



function renderDecks(data) {
    document.getElementById("loading").remove();
    
    var deckTemplate = document.getElementById("deck-template");

    for (const deck of data){
        var newDeck = deckTemplate.cloneNode(true);
        
        newDeck.id = deck._id.$oid;
        newDeck.getElementsByClassName("deck-name")[0].innerHTML = deck.name;
        newDeck.getElementsByClassName("deck-desc")[0].innerHTML = deck.description;

        for (const element of newDeck.getElementsByClassName("href-id")) {
            element.setAttribute( element.getAttribute("href").replace("_deck_id_", deck._id.$oid ));
            element.removeClass("href-id");
        }

        document.getElementById("deck-container").appendChild(newDeck);
    }
    deckTemplate.remove();
}
