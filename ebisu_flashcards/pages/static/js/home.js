loadDecks();

/*
 * Fills up all the fields which are deck-specific
 */ 
function deckRender(data, deck){
    // Hide feedback box
    feedback = deck.getElementsByClassName("feedback")[0].classList.add("hidden");
    
    // Render regular data into static view and form
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
    // Hide the loading icon
    hideLoadingIcon(deck);
}

/**
 * 
 * @param {*} deck 
 * @param {*} message 
 */
function renderIssue(deckId, message){
    deck = document.getElementById(deckId);
    feedback = deck.getElementsByClassName("feedback")[0];
    feedback.getElementsByTagName("p")[0].text = message;
    feedback.classList.remove("hidden");
}

/**
 * Validate the content of the deck form.
 * @param {} deck: deck box from DOM
 * @returns true if form is valid, false otherwise.
 */
function validateDeckForm(deckId){
    deck = document.getElementById(deckId);
    name_is_present = deck.getElementsByClassName("deck-name-form")[0].value != "";
    desc_is_present = deck.getElementsByClassName("deck-desc-form")[0].value != "";
    alg_is_present = deck.getElementsByClassName("deck-type-form")[0].value != "";
    
    if (name_is_present && desc_is_present && alg_is_present){
        return true;
    }
    return false;
}


function loadDecks(){
    callLoadBoxes('/api/decks', deckRender);
    getNewDeckAlgorithms();
}

function createNewDeck() {
    deckId = "create-box";
    showLoadingIcon(deckId);
    
    if (validateDeckForm(deckId)) {
        callCreateNewBox('/api/decks', deckRender);
    } else {
        renderIssue(deckId, "Please fill all the fields properly");
    }
}

function updateDeck(deckId) {
    showLoadingIcon(deckId);
    deck = document.getElementById(deckId);
    deck.getElementsByTagName("form")[0].classList.add("hidden");
    
    if (validateDeckForm(deckId)) {
        callUpdateBox(deckId, '/api/decks/'+deckId, deckRender);
    } else {
        renderIssue(deckId, "Please fill all the fields properly");
    }
}

function deleteDeck(deckId){
    confirmation = confirm("Are you sure you want to delete this deck?");
    if(confirmation){
        deck = document.getElementById("create-box");
        //showLoadingIcon(deck);
        callDeleteBox(deckId, '/api/decks/'+deckId);
    }
}

function getNewDeckAlgorithms(){
    callBackend(
        endpoint = '/api/algorithms',
        method = "GET",
        body = null, 
        callback = renderNewDeckAlgorithms
    )
}

function renderNewDeckAlgorithms(data){

    // Get the necessary element
    newBox = document.getElementById("create-box");
    extraFieldsTemplate = newBox.getElementsByClassName("extra-fields")[0];
    dropdown = newBox.getElementsByClassName("deck-type-form")[0];

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


function switchAlgorithmFields(){
    box = document.getElementById("create-box");
    algorithm = box.getElementsByClassName("deck-type-form")[0].value;

    for (extraFields of box.getElementsByClassName("extra-fields")) {
        extraFields.classList.add("hidden");
    }
    document.getElementById("extra-fields-"+algorithm).classList.remove("hidden");
}
