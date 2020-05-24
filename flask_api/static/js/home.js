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
        newDeck.getElementsByClassName("deck-type")[0].innerHTML = deck.algorithm;

        // Render deck id into the HREFs
        for (const element of newDeck.getElementsByTagName('a')) {
            const oldUrl = element.getAttribute("href");
            if (oldUrl) {
                element.setAttribute("href", oldUrl.replace("_deck_id_", deck._id.$oid ));
            }
        }
        for (const element of newDeck.getElementsByTagName('button')) {
            const oldValue = element.getAttribute("onclick");
            if (oldValue) {
                element.setAttribute("onclick", oldValue.replace("_deck_id_", deck._id.$oid ));
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


function showForm(deck_id) {
    // Disable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled")
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled")
        }    
    }
    // Disable New Deck button
    newDeckButton = document.getElementById('create-deck').getElementsByTagName("a")[0];
    newDeckButton.setAttribute("disabled", "disabled");

    // Find selected deck and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    template = document.getElementById('deck-form');

    // Clone the form & render deck id in buttons and links
    form = template.cloneNode(true);
    for (const element of form.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_deck_id_", deck_id ));
        }
    }
    for (const element of form.getElementsByTagName('button')) {
        const oldValue = element.getAttribute("onclick");
        if (oldValue) {
            element.setAttribute("onclick", oldValue.replace("_deck_id_", deck_id ));
        }
    }
    // Fill for with static data
    display = deck.getElementsByClassName("static-info")[0];
    form.getElementsByClassName("deck-name-form")[0].value = display.getElementsByClassName("deck-name")[0].textContent;
    form.getElementsByClassName("deck-desc-form")[0].value = display.getElementsByClassName("deck-desc")[0].textContent;
    form.getElementsByClassName("deck-name-form")[0].value = display.getElementsByClassName("deck-name")[0].textContent;

    // Clone the form into the selected deck & hide the static data
    display.classList.add("hidden");
    form.classList.remove("hidden");
    deck.appendChild(form);
}

function hideForm(deck_id) {
    // Find selected deck and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    console.log(deck);
    // Remove form
    deck.getElementsByTagName('form')[0].remove();
    // Make static info visible
    display = deck.getElementsByClassName("static-info")[0];
    display.classList.remove("hidden");
    // Enable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.removeAttribute("disabled")
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.removeAttribute("disabled")
        }    
    }
    // Enable New Deck button
    newDeckButton = document.getElementById('create-deck').getElementsByTagName("a")[0];
    newDeckButton.removeAttribute("disabled");

}