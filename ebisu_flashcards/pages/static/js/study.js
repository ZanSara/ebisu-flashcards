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
        }
    );
 }


function renderCard(data){
    console.log(data);

    // Save the card id for later
    window.localStorage.setItem("cardId", data._id.$oid);
    
    // Remove loading icon
    loading_icon = document.getElementById("loading");
    if(loading_icon !== null){
        document.getElementById("loading").remove();
    }

    // Ensure answer block is closed
    document.getElementById("collapsible").removeAttribute("open");

    // Clear the answer's field
    document.getElementById("guess").getElementsByTagName("input")[0].value = "";
    
    // Get the template box & remove the hiding class if present
    var cardBox = document.getElementById("card");
    cardBox.classList.remove("hidden");

    // Fill in question and answer
    document.getElementById("question").innerHTML = data.question_display;
    document.getElementById("answer").innerHTML = data.answer_display;

    // Sets CSRF tokens into forms
    for (const element of document.getElementsByClassName('csrf')) {
        element.value = getCookie("csrf_access_token");
    }
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
