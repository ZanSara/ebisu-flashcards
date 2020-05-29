/*
 * Invoked at load, renders every deck by copying the deck-template
 * and filling in the various values, taking them from the 'data' object.
 * 
 *      Required the 'data' object
 */
function renderDecks(data) {

    // Remove loading icon if present
    document.getElementById("loading").classList.add("hidden");
    
    // Get the template box
    var deckTemplate = document.getElementById("deck-template");

    for (const deck of data){
        // Clone template & remove the hiding class
        var newDeck = deckTemplate.cloneNode(true);
        newDeck.classList.remove("hidden");
        
        // Render proper data in the template
        newDeck.id = deck._id.$oid;
        newDeck.getElementsByClassName("deck-name")[0].innerHTML = deck.name;
        newDeck.getElementsByClassName("deck-name-form")[0].value = deck.name;
        newDeck.getElementsByClassName("deck-desc")[0].innerHTML = deck.description;
        newDeck.getElementsByClassName("deck-desc-form")[0].value = deck.description;
        newDeck.getElementsByClassName("deck-type")[0].innerHTML = deck.algorithm;
        newDeck.getElementsByClassName("deck-type-form")[0].value = deck.algorithm;

        // Append extra fields in form
        newDeck.getElementsByClassName("extra-fields")[0].innerHTML = deck.extra_fields;

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
    // Display the New Deck button
    createDeck = document.getElementById("create-deck");
    document.getElementById("deck-container").appendChild(createDeck);
    createDeck.classList.remove("hidden");
}


/* 
 * Invoked when clicking on the EDIT button of a static deck.
 * Swaps the static representation with the form representation.
 *   
 *      Requires the deck_id
 */
function showForm(deck_id) {

    // Find selected deck and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    display = deck.getElementsByClassName("static-info")[0];
    form = deck.getElementsByTagName("form")[0];

    // Disable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled");
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled");
        }    
    }
    // Disable New Deck button
    newDeckButton = document.getElementById('create-deck').getElementsByTagName("button")[0];
    newDeckButton.setAttribute("disabled", "disabled");

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Show the form of the selected deck & hide the static data
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

    // Find selected deck, the static data and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    display = deck.getElementsByClassName("static-info")[0];
    form = deck.getElementsByTagName('form')[0];

    // Enable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.removeAttribute("disabled");
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.removeAttribute("disabled");
        }    
    }
    // Enable New Deck button
    newDeckDiv = document.getElementById('create-deck');
    newDeckDiv.classList.remove("hidden");
    newDeckDiv.getElementsByTagName("button")[0].removeAttribute("disabled");     
    
    // Switch visibility between form and static data
    form.classList.add("hidden");
    display.classList.remove("hidden");
    
}


/* 
 * Invoked when clicking on the New Deck button.
 * Hides the button itself and adds a new div with an empty
 * form.
 */
function displayNewDeck() {
    // Find div
    deck = document.getElementById('create-deck');
    form = deck.getElementsByTagName("form")[0];
    button = deck.getElementsByTagName("button")[0];

    // Add the deck class to the div
    deck.classList.add("deck");
    
    // Disable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.setAttribute("disabled", "disabled")
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.setAttribute("disabled", "disabled")
        }    
    }
    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    
    // Hide and disable New Deck button
    button.setAttribute("disabled", "disabled");
    button.classList.add("hidden");
    // Show the form
    form.classList.remove("hidden");
}

/* 
 * Invoked when clicking on the Cancel button into a New Deck form.
 * Hides the form and restores the button
 */
function hideNewForm() {
    // Find div
    deck = document.getElementById('create-deck');
    form = deck.getElementsByTagName("form")[0];
    button = deck.getElementsByTagName("button")[0];
    
    // Enable all buttons for the decks
    for (const deck of document.getElementsByClassName('deck')){
        for (const element of deck.getElementsByTagName('button')) {
            element.removeAttribute("disabled");
        }
        for (const element of deck.getElementsByTagName('a')) {
            element.removeAttribute("disabled");
        }    
    }
    // Remove the deck class to the div
    deck.classList.remove("deck");
    // Hide the form
    form.classList.add("hidden");
    // Show the New Deck button
    button.removeAttribute("disabled");
    button.classList.remove("hidden");
    
}