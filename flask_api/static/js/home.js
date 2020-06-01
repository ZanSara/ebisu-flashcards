loadDecks();

/*
 * Fills up all the fields which are deck-specific
 */ 
function deckRender(data, deck){
    
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

}


function loadDecks(){
    callLoadBoxes('http://127.0.0.1:5000/api/decks', deckRender);
    getNewDeckAlgorithms();
}

function createNewDeck() {
    callCreateNewBox('http://127.0.0.1:5000/api/decks', deckRender);
}

function updateDeck(deckId) {
    callUpdateBox(deckId, 'http://127.0.0.1:5000/api/decks/'+deckId, deckRender);
}

function deleteDeck(deckId){
    callDeleteBox(deckId, 'http://127.0.0.1:5000/api/decks/'+deckId, deckRender);
}

function getNewDeckAlgorithms(){
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/algorithms',
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
