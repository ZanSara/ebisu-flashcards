/*
 * Spawns many new boxes at the end of the boxes list.
 * New Deck button is kept at the very end.
 */
function appendBoxes(data_list){

    var template = document.getElementById("deck-template");

    for (const data of data_list){
        var deck = createBox(data, template);
        document.getElementById("deck-container").appendChild(deck);
    }
    
    // Move the New Deck button after the box
    createDeck = document.getElementById("create-deck");
    document.getElementById("deck-container").appendChild(createDeck);
}


/*
 * Spawns a new box at the end of the boxes list.
 * New Deck button is kept at the very end.
 */
function appendBox(data){
    appendBoxes([data]);
}



/*
 * Invoked at load, renders every deck using the data
 * received from the caller.
 */
function initialDecksRendering(decks_list) {

    // Remove loading icon if present
    document.getElementById("loading").classList.add("hidden");
    
    appendBoxes(decks_list);

    // Display the New Deck button & reset its form for good measure
    createDeck = document.getElementById("create-deck");
    createDeck.classList.remove("hidden");
    createDeck.getElementsByTagName("form")[0].reset();
}


/*
 * Updates the representation of a single deck,
 * either creating a box, updating an existing one, 
 * or deleting one.
 */
function updateDeckData(data, deck_id){
    
    if (data === ""){
        // Deck was deleted: delete its div (deck_id must be defined)
        deleteBox(""+deck_id);

    } else {
        if (deck_id) {
            // Existing deck - update its box
            deck = document.getElementById(""+deck_id);
            updateBox(data, deck);

        } else {
            // New Deck - create a box for it
            appendBox(data);
        }
    }
}

/* 
 * Invoked when clicking on the EDIT button of a static deck.
 * Swaps the static representation with the form representation.
 *   
 *      Requires the deck_id
 */
function showForm(deck_id) {

    pageModeEdit();    

    // Find selected deck and the form template
    deck = document.getElementById(""+deck_id);  // Necessary to make deck_id a string and match
    display = deck.getElementsByClassName("static-info")[0];
    form = deck.getElementsByTagName("form")[0];

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
    pageModeRead();
}

/* 
 * Invoked when clicking on the New Deck button.
 * Hides the button itself and adds a new div with an empty
 * form.
 */
function showNewForm() {

    pageModeEdit();

    // Find div
    deck = document.getElementById('create-deck');
    form = deck.getElementsByTagName("form")[0];
    button = deck.getElementsByTagName("button")[0];

    // Add the box class to the div
    deck.classList.add("box");

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Hide the New Deck button
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

    pageModeRead();

    // Find div
    deck = document.getElementById('create-deck');
    form = deck.getElementsByTagName("form")[0];
    button = deck.getElementsByTagName("button")[0];
    
    // Remove the box class to the div
    deck.classList.remove("box");
    
    // Show the New Deck button
    button.removeAttribute("disabled");
    button.classList.remove("hidden");
}


function switchExtraFields(){
    deck = document.getElementById("create-deck");
    algorithm = deck.getElementsByClassName("deck-type-form")[0].value;

    for (extraFields of deck.getElementsByClassName("extra-fields")) {
        extraFields.classList.add("hidden");
    }

    document.getElementById("extra-fields-"+algorithm).classList.remove("hidden");
}





/*
 * Sets up the algorithm options in the New Deck form.
 *      
 *      Requires data
 */
function renderNewDeckAlgorithms(data){

    // Get the necessary element
    createDeck = document.getElementById("create-deck");
    extraFieldsTemplate = createDeck.getElementsByClassName("extra-fields")[0];
    dropdown = createDeck.getElementsByClassName("deck-type-form")[0];

    for (const algorithm of data) {

        // Append algorithm name to the dropdown
        var option = document.createElement("option");
        option.text = algorithm.name;
        dropdown.add(option); 

        // Append hidden extra fields block
        extraFields = extraFieldsTemplate.cloneNode(true);
        extraFields.id = "extra-fields-"+algorithm.name;
        extraFields.innerHTML = algorithm.extra_fields;
        extraFields.classList.add("hidden");
        // Append right after the template
        extraFieldsTemplate.parentNode.insertBefore(extraFields, extraFieldsTemplate.nextSibling);
    }
}