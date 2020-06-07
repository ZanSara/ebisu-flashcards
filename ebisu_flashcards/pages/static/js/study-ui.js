
function renderCard(data){
    console.log(data);

    // Save the card id for later
    window.localStorage.setItem("cardId", data._id.$oid);
    
    // Remove loading icon
    loading_icon = document.getElementById("loading");
    if(loading_icon !== null){
        document.getElementById("loading").remove();
    }

    // Hide the No Cards block if necessary
    var noCardsBox = document.getElementById("no-cards");
    noCardsBox.classList.add("hidden");

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


function renderRemoteErrors(response){
    
    // Remove loading icon
    loading_icon = document.getElementById("loading");
    if(loading_icon !== null){
        document.getElementById("loading").remove();
    }

    // Get the box & remove the hiding class
    var noCardsBox = document.getElementById("no-cards");
    noCardsBox.classList.remove("hidden");

    // Renders deckId where necessary
    deckId = window.localStorage.getItem("deckId");
    for (const element of document.getElementsByTagName('a')) {
        const oldUrl = element.getAttribute("href");
        if (oldUrl) {
            element.setAttribute("href", oldUrl.replace("_deck_id_", deckId ));
        }
    }
}

