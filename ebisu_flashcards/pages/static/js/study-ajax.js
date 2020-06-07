/* Save the deckId in the local storage for quicker access */
window.localStorage.setItem("deckId", window.location.pathname.split('/').pop());

// Run at page load
fetchCard();


function fetchCard(){
    deckId = window.localStorage.getItem("deckId");
    callBackend(
        endpoint='/api/study/'+deckId,
        method = "GET",
        body = null,
        callback = function(data) {
            while (document.readyState === "loading") {};
            renderCard(data);
        },
        errorCallback = renderRemoteErrors
    );
}


function submitResults(value){

    deckId = window.localStorage.getItem("deckId");
    cardId = window.localStorage.getItem("cardId");
    callBackend(
        endpoint='/api/study/'+deckId,
        method = "POST",
        body = JSON.stringify({'test_results': value, 'card_id': cardId}),
        callback = function(data) {
            fetchCard(); 
        }
    );
    return false;
}
