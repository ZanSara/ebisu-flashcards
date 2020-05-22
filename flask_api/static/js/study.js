// I should have a CSRF token set after logging in
var token = getCookie("csrf_access_token");

// Read the deck id from the URL
var deck_id = window.location.href.split("/").pop();

// Fetch card data
fetch('http://127.0.0.1:5000/api/study/'+deck_id, 
    {   
        method:'GET',
        headers:  new Headers({'Authorization': 'Bearer '+token}),
    })
.then(res => res.json())
.then((data) => {
    while (document.readyState === "loading") {};
    renderCard(data);
})
.catch(console.log);  /* TODO: HANDLE BETTER */


function renderCard(data){
    console.log(data);

    // Remove loading icon
    document.getElementById("loading").remove();
    
    // Get the template box & remove the hiding class
    var cardBox = document.getElementById("card");
    cardBox.classList.remove("hidden");
}