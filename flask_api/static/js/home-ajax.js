loadDecks();


function loadDecks(){
    callBackend(
        endpoint='http://127.0.0.1:5000/api/decks',
        method = "GET",
        body = null,
        callback = function(data) {
            // Wait for the page to be loaded
            while (document.readyState === "loading") {};
            getNewDeckAlgorithms();
            initialDecksRendering(data);
        }
    )
}

function createNewDeck() {
    form = document.getElementById("create-deck").getElementsByTagName("form")[0];
    form = serializeForm(form);

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks',
        method = "POST",
        body = form,
        callback = function(data){
            hideNewForm();
            updateDeckData(data);
        }
    )
}

function updateDeck(deck_id) {
    form = document.getElementById(""+deck_id).getElementsByTagName("form")[0];
    form = serializeForm(form)

    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deck_id, 
        method = "PUT",
        body = form,
        callback = function(data){
            hideForm(deck_id);
            updateDeckData(data, deck_id);
        }
    )
}

function deleteDeck(deck_id) {
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/decks/'+deck_id, 
        method = 'DELETE',
        body = null,
        callback = function(data){
            hideForm(deck_id);
            updateDeckData(data, deck_id);
        }
    )
}

function getNewDeckAlgorithms(){
    callBackend(
        endpoint = 'http://127.0.0.1:5000/api/algorithms',
        method = "GET",
        body = null, 
        callback = renderNewDeckAlgorithms
    )
}
