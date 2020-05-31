/*
 * Spawns many new boxes at the end of the boxes list.
 * New card button is kept at the very end.
 */
function appendBoxes(data_list){

    var template = document.getElementById("card-template");

    for (const data of data_list){
        var card = createBox(data, template);
        document.getElementById("cards-container").appendChild(card);
    }
    
    // Move the New card button after the box
    createcard = document.getElementById("create-card");
    document.getElementById("cards-container").appendChild(createcard);
}


/*
 * Spawns a new box at the end of the boxes list.
 * New card button is kept at the very end.
 */
function appendBox(data){
    appendBoxes([data]);
}



/*
 * Invoked at load, renders every card using the data
 * received from the caller.
 */
function initialCardsRendering(cards_list) {

    // Remove loading icon if present
    document.getElementById("loading").classList.add("hidden");
    
    appendBoxes(cards_list);

    // Display the New card button & reset its form for good measure
    createcard = document.getElementById("create-card");
    createcard.classList.remove("hidden");
    createcard.getElementsByTagName("form")[0].reset();
}


/*
 * Updates the representation of a single card,
 * either creating a box, updating an existing one, 
 * or deleting one.
 */
function updateCardData(data, card_id){
    
    if (data === ""){
        // card was deleted: delete its div (card_id must be defined)
        deleteBox(""+card_id);

    } else {
        if (card_id) {
            // Existing card - update its box
            card = document.getElementById(""+card_id);
            updateBox(data, card);

        } else {
            // New card - create a box for it
            appendBox(data);
        }
    }
}

/* 
 * Invoked when clicking on the EDIT button of a static card.
 * Swaps the static representation with the form representation.
 *   
 *      Requires the card_id
 */
function showForm(card_id) {

    pageModeEdit();    

    // Find selected card and the form template
    card = document.getElementById(""+card_id);  // Necessary to make card_id a string and match
    display = card.getElementsByClassName("static-info")[0];
    form = card.getElementsByTagName("form")[0];

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Show the form of the selected card & hide the static data
    display.classList.add("hidden");
    form.classList.remove("hidden");
    card.appendChild(form);
}


/* 
 * Invoked when clicking on the CANCEL button of a card form.
 * Swaps the form representation with the static representation.
 *   
 *      Requires the card_id
 */
function hideForm(card_id) {
    pageModeRead();
}

/* 
 * Invoked when clicking on the New card button.
 * Hides the button itself and adds a new div with an empty
 * form.
 */
function showNewForm() {

    pageModeEdit();

    // Find div
    card = document.getElementById('create-card');
    form = card.getElementsByTagName("form")[0];
    button = card.getElementsByTagName("button")[0];

    // Add the card class to the div
    card.classList.add("box");

    // Enable back form buttons
    for (const element of form.getElementsByTagName('button')) {
        element.removeAttribute("disabled");
    }
    for (const element of form.getElementsByTagName('a')) {
        element.removeAttribute("disabled");
    }    

    // Hide the New card button
    button.setAttribute("disabled", "disabled");
    button.classList.add("hidden");

    // Show the form
    form.classList.remove("hidden");
}

/* 
 * Invoked when clicking on the Cancel button into a New card form.
 * Hides the form and restores the button
 */
function hideNewForm() {

    pageModeRead();

    // Find div
    card = document.getElementById('create-card');
    form = card.getElementsByTagName("form")[0];
    button = card.getElementsByTagName("button")[0];
    
    // Remove the card class to the div
    card.classList.remove("box");
    
    // Show the New card button
    button.removeAttribute("disabled");
    button.classList.remove("hidden");
}


function switchExtraFields(){
    card = document.getElementById("create-card");
    algorithm = card.getElementsByClassName("card-type-form")[0].value;

    for (extraFields of card.getElementsByClassName("extra-fields")) {
        extraFields.classList.add("hidden");
    }

    document.getElementById("extra-fields-"+algorithm).classList.remove("hidden");
}





/*
 * Sets up the algorithm options in the New card form.
 *      
 *      Requires data
 */
function renderNewcardAlgorithms(data){

    // Get the necessary element
    createcard = document.getElementById("create-card");
    extraFieldsTemplate = createcard.getElementsByClassName("extra-fields")[0];
    dropdown = createcard.getElementsByClassName("card-type-form")[0];

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