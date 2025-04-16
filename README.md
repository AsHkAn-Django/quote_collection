# Quote Collection App  
An enhanced Django quote app with likes, AJAX updates, and threaded comments.

## Features  
- Like/Unlike quotes with AJAX (no page refresh)  
- Add and reply to comments (nested)  
- Dynamic updates using JavaScript  

## Installation  
```bash
git clone https://github.com/yourusername/quote-interact.git  
cd quote_collection  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver
```
## Usage
- Create an account and log in.
- Like/unlike quotes instantly.
- Add and reply to comments.

## Models
- Quote: Stores quotes.
- Like: Links users to liked quotes.
- Comment: Stores user comments with replies.

## AJAX Setup
- Use fetch() in JavaScript to send like requests.

Update like counts dynamically with JSON responses.


## Tutorial

For sync like button first we need our models
```python
class Quote(models.Model):
    body = models.CharField(max_length=500)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=260)
    like_numbers = models.PositiveSmallIntegerField(default=0)
    
    def count_likes(self):
        counter = Like.objects.filter(quote=self).count()
        self.like_numbers = counter
        self.save()
        return counter

    def __str__(self):
        return f"{self.author}: {self.body[:50]}..."

    def get_absolute_url(self):
        return reverse('quote_detail', kwargs={'pk': self.pk})

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Liked {self.quote.author} quote"
```

Then the views for it
```python
def like(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    
    if request.method == 'POST':
        like_object = Like.objects.filter(user=request.user, quote=quote)
        
        # Toggle like status
        if like_object.exists():
            like_object.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, quote=quote)
            liked = True
        
        # Return a JSON response with the new like status
        return JsonResponse({
            'liked': liked,
            'like_count': quote.count_likes(),  # You can modify this to show the total like count
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
```

And the url for the view ofcourse:)
```python
path('quote/quote_list/like/<int:pk>/', views.like, name='like'),
```

the html for representing it
```html
 {% for quote in quotes %}
    <div class="container mt-5">
        <div class="container mt-5">
          <div class="p-5 text-center bg-body-tertiary rounded-3 mb-4">
          <figcaption class="blockquote-header text-center text-white bg-secondary">
            Published By <cite title="Source Title">{{ quote.publisher }}</cite>
          </figcaption>
          <figure class="text-center">
              <blockquote class="blockquote">
                <p>{{ quote.body }}</p>
              </blockquote>
              <figcaption class="blockquote-footer">
                By <cite title="Source Title">{{ quote.author }}</cite>
              </figcaption>
              <button class="btn btn-outline-danger like-button" 
                data-quote-id="{{ quote.pk }}" 
                data-liked="{{ quote.liked }}">
                {% if quote.liked %}
                  Unlike
                {% else %}
                  Like
                {% endif %}
                </button>
                <span class="m-3">{{ quote.count_likes }} likes & {{ quote.comments_num }} comments</span>
                <div>
                  <a href="{% url 'quote_detail' quote.id %}">more</a> 
                </div>
              </div>
          </figure>
        </div>
    </div>
    </div>      
  {% endfor %}
```

and at the end the js for sync it
```js
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
```
---


### Using annotate to add field name comments_num to the qurryset for showing the number of comments for each quote
```python
class QuoteListView(LoginRequiredMixin, generic.ListView):
    model = Quote
    template_name = 'myApp/quote_list.html'
    context_object_name = 'quotes'
    
    def get_queryset(self):
        user = self.request.user
        queryset = Quote.objects.annotate(
            # This part is for adding a boolean to the field liked that is related to the previous topic not this one
            liked=Exists(Like.objects.filter(user=user, quote=OuterRef('pk')))).annotate(
                # here we have two models to count comments and sub_comments and after counting we add them easily
                comments_num=(Count('comments', distinct=True) + Count('comments__sub_comments', distinct=True)))
                # Now we have a field name comments_num that contains the sum of comments and sub_comments
        return queryset
```

## License
### MIT
```vbnet
Let me know if you need any refinements! 🚀
```

## Tags  
#django #tutorial #beginner-friendly #web-development #ajax #like-system #quotes-app #python #django-project
