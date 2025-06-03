document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const quoteId = this.getAttribute('data-quote-id');
            const liked = this.getAttribute('data-liked') === 'true';  
            const csrftoken = document.getElementById("csrf_token").value;  // Get CSRF token

            
            fetch(`/quote/quote_list/like/${quoteId}/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken     // Use CSRF token from hidden input
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
