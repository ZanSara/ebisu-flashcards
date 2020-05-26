/*
 * Invoked at load, renders every deck by copying the deck-template
 * and filling in the various values, taking them from the 'data' object.
 * 
 *      Required the 'data' object
 */
function renderDecks(data) {

    // Remove loading icon
    document.getElementById("loading").remove();
    
    // Get the template box
    var deckTemplate = document.getElementById("deck-template");

    for (const deck of data){
        // Clone template & remove the hiding class
        var newDeck = deckTemplate.cloneNode(true);
        newDeck.classList.remove("hidden");
        
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

    // Append New Deck box to the end & display
    createDeck = document.getElementById("create-deck");
    document.getElementById("deck-container").appendChild(createDeck);
    createDeck.classList.remove("hidden");
}


/* 
 * Invoked when clicking on the EDIT button of a static deck.
 * Swaps the static representation with the form representation,
 * also filling the form with the proper values.
 *   
 *      Requires the deck_id
 */
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
    newDeckButton = document.getElementById('create-deck').getElementsByTagName("button")[0];
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


/* 
 * Invoked when clicking on the CANCEL button of a deck form.
 * Swaps the form representation with the static representation.
 *   
 *      Requires the deck_id
 */
function hideForm(deck_id) {

    // Find selected deck and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    console.log(deck);

    if (deck_id === "new-deck") {
        // Remove entire deck
        deck.remove();

    } else {
        // Remove form
        deck.getElementsByTagName('form')[0].remove();

        // Make static info visible
        display = deck.getElementsByClassName("static-info")[0];
        display.classList.remove("hidden");
    }

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
    newDeckDiv = document.getElementById('create-deck');
    newDeckDiv.classList.remove("hidden");
    newDeckDiv.getElementsByTagName("button")[0].removeAttribute("disabled");      
}


/* 
 * Invoked when clicking on the New Deck button.
 * Hides the button itself and adds a new div with an empty
 * form.
 */
function newDeck() {

    // Disable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled")
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled")
        }    
    }
    // Hide New Deck button
    newDeckDiv = document.getElementById('create-deck');
    newDeckDiv.getElementsByTagName("button")[0].setAttribute("disabled", "disabled");
    newDeckDiv.classList.add("hidden");

    // Find the deck and form templates & clone them
    deck = document.getElementById('deck-template').cloneNode(true);
    deck.id = "new-deck"
    form = document.getElementById('deck-form').cloneNode(true);

    // Render deck id in buttons and links
    for (const element of form.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_deck_id_", "new-deck" ));
        }
    }
    for (const element of form.getElementsByTagName('button')) {
        const oldValue = element.getAttribute("onclick");
        if (oldValue) {
            element.setAttribute("onclick", oldValue.replace("_deck_id_", "new-deck" ));
        }
    }
    
    // Hide static info data
    deck.getElementsByClassName("static-info")[0].classList.add("hidden")

    // Clone the form into the selected deck & hide the static data
    form.classList.remove("hidden");
    deck.appendChild(form);

    // Append the new element and display it
    document.getElementById("deck-container").appendChild(deck);
    deck.classList.remove("hidden");
}