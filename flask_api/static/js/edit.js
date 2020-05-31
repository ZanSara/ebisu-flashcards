
/* Save the deckId in the local storage for quicker access */
window.localStorage.setItem("deckId", window.location.pathname.split('/').pop());


loadCards();


/*
 * Fills up all the fields which are card-specific
 */ 
function cardRender(data, card){
    card.getElementsByClassName("question")[0].innerHTML = data.question;
    card.getElementsByClassName("question-form")[0].value = data.question;
    card.getElementsByClassName("answer")[0].innerHTML = data.answer;
    card.getElementsByClassName("answer-form")[0].value = data.answer;
}


function loadCards(){
    deckId = window.localStorage.getItem("deckId");
    loadBoxes('http://127.0.0.1:5000/api/decks/'+deckId+'/cards', cardRender);
    //getNewCardAlgorithms();
}

function createNewCard() {
    deckId = window.localStorage.getItem("deckId");
    createNewBox('http://127.0.0.1:5000/api/decks/'+deckId+'/cards', cardRender);
}

function updateCard(cardId) {
    deckId = window.localStorage.getItem("deckId");
    updateBox(cardId, 'http://127.0.0.1:5000/api/decks/'+deckId+'/cards/'+cardId, cardRender);
}

function deleteCard(cardId){
    deckId = window.localStorage.getItem("deckId");
    deleteBox(cardId, 'http://127.0.0.1:5000/api/decks/'+deckId+'/cards/'+cardId, cardRender);
}









function getNewCardAlgorithms(){
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/algorithms',
        method = "GET",
        body = null, 
        callback = renderNewCardAlgorithms
    )
}

function renderNewCardAlgorithms(data){

    // Get the necessary element
    newBox = document.getElementById("create-box");
    extraFieldsTemplate = newBox.getElementsByClassName("extra-fields")[0];
    dropdown = newBox.getElementsByClassName("card-type-form")[0];

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
    algorithm = box.getElementsByClassName("card-type-form")[0].value;

    for (extraFields of box.getElementsByClassName("extra-fields")) {
        extraFields.classList.add("hidden");
    }

    document.getElementById("extra-fields-"+algorithm).classList.remove("hidden");
}
