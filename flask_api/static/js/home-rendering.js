/* 
 * Given a deck data and a box,
 * returns a box with the updated data rendered in.
 */
function updateBox(data, deck){
    
    // Render proper data in the template
    deck.id = data._id.$oid;
    deck.getElementsByClassName("deck-name")[0].innerHTML = data.name;
    deck.getElementsByClassName("deck-name-form")[0].value = data.name;
    deck.getElementsByClassName("deck-desc")[0].innerHTML = data.description;
    deck.getElementsByClassName("deck-desc-form")[0].value = data.description;
    deck.getElementsByClassName("deck-type")[0].innerHTML = data.algorithm;
    deck.getElementsByClassName("deck-type-form")[0].value = data.algorithm;

    // Append extra fields in form
    extraFields = deck.getElementsByClassName("extra-fields")[0];
    extraFields.innerHTML = data.extra_fields;

    // Render the extra field values
    for (const input of extraFields.querySelectorAll("input[type=checkbox]")){
        input.checked = data[input.name];
    }

    // Render deck id into the HREFs
    for (const element of deck.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_deck_id_", data._id.$oid ));
        }
    }
    for (const element of deck.getElementsByTagName('button')) {
        const oldValue = element.getAttribute("onclick");
        if (oldValue) {
            element.setAttribute("onclick", oldValue.replace("_deck_id_", data._id.$oid ));
        }
    }
    // Return rendered deck
    return deck;
}



/* 
 * Given a deck data and the template, 
 * returns a new box with the new data rendered in.
 */
function createBox(data, template){

    // Clone template & remove the hiding class
    var deck = template.cloneNode(true);
    deck.classList.remove("hidden");
    
    updateBox(data, deck);

    // Return rendered copy
    return deck;
}



/* 
 * Given a deck id, removes its box.
 * Fails if box does not exits.
 */
function deleteBox(deck_id){
    document.getElementById(deck_id).remove();
}



/* 
 * Puts the page into Read Mode 
 * (no visible forms)
 */
function pageModeRead(){

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

    // Hide all forms 
    forms = document.getElementsByTagName('form');
    for (const form of forms){
        form.classList.add("hidden");
    }
    
    // Display all static-info
    displays = deck.getElementsByClassName("static-info");
    for (const display of displays){
        display.classList.remove("hidden");
    }    
    
    // Reset the NewDeck form & hide all extra fields
    form = document.getElementById('create-deck').getElementsByTagName("form")[0];
    form.reset();
    for (const fields of form.getElementsByClassName("extra-fields")){
        fields.classList.add("hidden");
    }
}



/* 
 * Puts the page into Edit Mode 
 * (everything disabled, caller should re-enable its components) 
 */
function pageModeEdit(){
    
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
}
