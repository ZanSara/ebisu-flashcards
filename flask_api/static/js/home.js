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
    // Remove loading icon
    document.getElementById("loading").remove();
    
    // Get the template box & remove the hiding class
    var deckTemplate = document.getElementById("deck-template");
    deckTemplate.classList.remove("hidden");

    for (const deck of data){
        // Clone template
        var newDeck = deckTemplate.cloneNode(true);
        
        // Render proper data in the template
        newDeck.id = deck._id.$oid;
        newDeck.getElementsByClassName("deck-name")[0].innerHTML = deck.name;
        newDeck.getElementsByClassName("deck-desc")[0].innerHTML = deck.description;

        // Render deck id into the HREFs
        for (const element of newDeck.getElementsByTagName('a')) {
            const oldUrl = element.getAttribute("href");
            if (oldUrl) {
                element.setAttribute("href", oldUrl.replace("_deck_id_", deck._id.$oid ));
            }
        }
        // Append rendered copy
        document.getElementById("deck-container").appendChild(newDeck);
    }
    // Remove template
    deckTemplate.remove();

    // Append New Deck box to the end & display
    createDeck = document.getElementById("create-deck");
    document.getElementById("deck-container").appendChild(createDeck);
    createDeck.classList.remove("hidden");
}
