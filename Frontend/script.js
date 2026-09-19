const form = document.getElementById("urlForm");
const result = document.getElementById("result");

const API_URL = "https://keud9j3hlf.execute-api.eu-south-2.amazonaws.com";

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const url = document.getElementById("urlInput").value;

    result.textContent = "Creating short URL...";

    try {
        const response = await fetch(`${API_URL}/shorten`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong");
        }

        const shortUrl = `${API_URL}/${data.shortCode}`;

        result.innerHTML = `
            <p>Short URL created:</p>
            <a href="${shortUrl}" target="_blank">${shortUrl}</a>
        `;

    } catch (error) {
        console.error(error);
        result.textContent = "Error: " + error.message;
    }
});
