
/* Save the deckId in the local storage for quicker access */
window.localStorage.setItem("deckId", window.location.pathname.split('/').pop());


loadCards();


/*
 * Fills up all the fields which are card-specific
 */ 
function cardRender(data, card){
    card.getElementsByClassName("question")[0].innerHTML = data.question_display;
    card.getElementsByClassName("question-form")[0].innerHTML = data.question_form;
    card.getElementsByClassName("answer")[0].innerHTML = data.answer_display;
    card.getElementsByClassName("answer-form")[0].innerHTML = data.answer_form;
}


function loadCards(){
    deckId = window.localStorage.getItem("deckId");
    callLoadBoxes('/api/decks/'+deckId+'/cards', cardRender);
    getNewCardFields('question');
    getNewCardFields('answer');
}

function createNewCard() {
    deckId = window.localStorage.getItem("deckId");
    callCreateNewBox('/api/decks/'+deckId+'/cards', cardRender);
}

function updateCard(cardId) {
    deckId = window.localStorage.getItem("deckId");
    callUpdateBox(cardId, '/api/decks/'+deckId+'/cards/'+cardId, cardRender);
}

function deleteCard(cardId){
    deckId = window.localStorage.getItem("deckId");
    callDeleteBox(cardId, '/api/decks/'+deckId+'/cards/'+cardId);
}

function getNewCardFields(prefix){
    callBackend(
        endpoint = '/api/'+prefix+'-templates',
        method = "GET",
        body = null, 
        callback = renderNewCardFields,
        errorCallback = reportError,
        params = prefix
    )
}

function renderNewCardFields(data, prefix){
    // Get the necessary element
    newBox = document.getElementById("create-box");
    fieldTypeFormTemplate = newBox.getElementsByClassName(""+prefix+"-fields")[0];
    dropdown = newBox.getElementsByClassName(""+prefix+"-field-type-form")[0];

    for (const fieldType of data) {

        // Append fieldType name to the dropdown
        var option = document.createElement("option");
        option.text = fieldType.name;
        dropdown.add(option); 

        // Append hidden extra fields block
        fieldTypeForm = fieldTypeFormTemplate.cloneNode(true);
        fieldTypeForm.id = ""+prefix+"-fields-"+fieldType.name;
        fieldTypeForm.innerHTML = fieldType.form_html;
        fieldTypeForm.classList.add("hidden");
        // Append right after the template
        fieldTypeFormTemplate.parentNode.insertBefore(fieldTypeForm, fieldTypeFormTemplate.nextSibling);
    }
}


function switchFieldType(prefix){
    box = document.getElementById("create-box");
    fieldType = box.getElementsByClassName(""+prefix+"-field-type-form")[0].value;

    for (extraFields of box.getElementsByClassName(""+prefix+"-fields")) {
        extraFields.classList.add("hidden");
    }
    document.getElementById(""+prefix+"-fields-"+fieldType).classList.remove("hidden");
}
