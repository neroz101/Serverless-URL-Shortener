const form = document.getElementById("urlForm");
const result = document.getElementById("result");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    const url = document.getElementById("urlInput").value;

    result.textContent =
        "URL received: " + url;

});
