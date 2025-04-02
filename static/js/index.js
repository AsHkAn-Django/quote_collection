let csrfToken = "";

// Fetch CSRF Token
fetch("/get-csrf-token/")
    .then(response => response.json())
    .then(data => {
        csrfToken = data.csrfToken;  // Store CSRF token
    })
    .catch(error => console.error("Error fetching CSRF token:", error));


document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const quoteId = this.getAttribute('data-quote-id');
            const liked = this.getAttribute('data-liked') === 'true';  
            
            fetch(`/quote/quote_list/like/${quoteId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  
                },
                body: JSON.stringify({})  
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked !== undefined) {
                    // Update button text
                    if (data.liked) {
                        this.textContent = 'Unlike';
                    } else {
                        this.textContent = 'Like';
                    }

                    // Update the like count
                    this.nextElementSibling.textContent = `${data.like_count} likes`;   
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
