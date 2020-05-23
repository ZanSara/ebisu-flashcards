// Run at page load
fetchCard();


function fetchCard(){
    // I should have a CSRF token set after logging in
    var csrf_token = getCookie("csrf_access_token");

    // Read the deck id from the URL
    var deck_id = window.location.href.split("/").pop();

    // Fetch card data
    fetch('http://127.0.0.1:5000/api/study/'+deck_id, 
        {   
            method:'GET',
            headers:  new Headers({'Authorization': 'Bearer ' + csrf_token}),
        })
    .then(res => res.json())
    .then((data) => {
        while (document.readyState === "loading") {};
        renderCard(data);
    })
    .catch(console.log);  /* TODO: HANDLE BETTER */
 };


function renderCard(data){
    console.log(data);

    // Remove loading icon
    loading_icon = document.getElementById("loading");
    if(loading_icon !== null){
        document.getElementById("loading").remove();
    }

    // Ensure answer block is closed
    document.getElementById("collapsible").removeAttribute("open");
    
    // Get the template box & remove the hiding class if present
    var cardBox = document.getElementById("card");
    cardBox.classList.remove("hidden");

    // Fill in question and answer
    document.getElementById("question").innerHTML = data.question;
    document.getElementById("answer").innerHTML = data.answer;

    // Sets CSRF tokens into forms
    for (const element of document.getElementsByClassName('csrf')) {
        element.value = getCookie("csrf_access_token");
    }
}

function submitResults(value){
    
    // Gather the tokens
    var access_token = getCookie("access_token-cookie");
    var csrf_token = getCookie("csrf_access_token");

    // Read the deck id from the URL
    var deck_id = window.location.href.split("/").pop();

    // Submit results to the FORM action endpoint
    fetch('http://127.0.0.1:5000/api/study/'+deck_id, 
    {   
        method:'POST',
        headers:  new Headers({
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'X-CSRF-TOKEN': csrf_token,
        }),
        body: JSON.stringify({'test_results': value}),
        credentials: 'include'
    })
    .then(res => res.json())
    .then((data) => {
        fetchCard();    
    }).catch(console.log);  /* TODO: HANDLE BETTER */

    return false;
}
