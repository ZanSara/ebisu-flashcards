
// Save the deckId in the local storage
window.localStorage.setItem("deckId", window.location.pathname.split('/').pop());

loadCards();


function loadCards(){
    deckId = window.localStorage.getItem("deckId");
    callBackend(
        endpoint='http://127.0.0.1:5000/api/decks/'+deckId+"/cards",
        method = "GET",
        body = null,
        callback = function(data) {
            // Wait for the page to be loaded
            while (document.readyState === "loading") {};
            initialCardsRendering(data);
        }
    )
}

function createNewCard() {
    deckId = window.localStorage.getItem("deckId");

    form = document.getElementById("create-card").getElementsByTagName("form")[0];
    form = serializeForm(form);

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deckId+"/cards",
        method = "POST",
        body = form,
        callback = function(data){
            hideNewForm();
            updateCardData(data);
        }
    )
}

function updateCard(cardId) {
    deckId = window.localStorage.getItem("deckId");

    form = document.getElementById(""+cardId).getElementsByTagName("form")[0];
    form = serializeForm(form)

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deckId+"/cards/"+cardId, 
        method = "PUT",
        body = form,
        callback = function(data){
            hideForm(cardId);
            updateCardData(data, cardId);
        }
    )
}

function deleteCard(cardId) {
    deckId = window.localStorage.getItem("deckId");

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deckId+"/cards/"+cardId, 
        method = 'DELETE',
        body = null,
        callback = function(data){
            hideForm(cardId);
            updateCardData(data, cardId);
        }
    )
}