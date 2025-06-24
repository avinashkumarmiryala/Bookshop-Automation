document.addEventListener("DOMContentLoaded", () => {
    const searchResultsSection = document.getElementById("SearchResults");
    const resultContainer = document.getElementById("ResultContainer");
    const slideshowSection = document.querySelector(".slider-section");

    // Hide search results initially
    searchResultsSection.style.display = "none";

    // Function to handle searches
    async function searchBooks(query, type) {
        if (!query) {
            alert(`Please enter a ${type} to search.`);
            return;
        }

        // Hide slideshow and show search results
        slideshowSection.style.display = "none";
        searchResultsSection.style.display = "block";

        try {
            const endpoint = type === "title" ? `/search_book_by_title/` : `/search_book_by_author/`;
            const fullUrl = `http://127.0.0.1:5000${endpoint}${encodeURIComponent(query)}`;
            
            console.log("Requesting URL:", fullUrl);
            
            const response = await fetch(fullUrl);
            const data = await response.json();

            console.log("Raw search data:", data);
            console.log("Data type:", typeof data, Array.isArray(data));
            
            // Clear previous results
            resultContainer.innerHTML = "";

            // Better handling of different response formats
            let booksArray = [];
            let booksHTML = '';
            
            if (Array.isArray(data)) {
                // If data is already an array
                booksArray = data;
            } else if (typeof data === 'object') {
                if (data.hasOwnProperty('message')) {
                    // No books found message
                    booksHTML = `<p>No books found for "${query}".</p>`;
                } else {
                    // Single book object
                    booksArray = [data];
                }
            }

            // Display message if no books found or empty array
            if (booksArray.length === 0 && booksHTML === '') {
                booksHTML = `<p>No books found for "${query}".</p>`;
            } else {
                // Generate HTML for books
                booksArray.forEach(book => {
                    const imageUrl = book.image_url;
                    booksHTML += `
                        <div class="book-card">
                            <img src="${imageUrl}" alt="${book.title}" class="book-image">
                            <div class="book-details">
                                <p><strong>Title:</strong> ${book.title}</p>
                                <p><strong>Author:</strong> ${book.author}</p>
                                <p><strong>ISBN:</strong> ${book.isbn}</p>
                                <p><strong>Stock:</strong> ${book.stock}</p>
                                <p><strong>Rack:</strong> ${book.rack}</p>
                                <div class="cart-controls">
                                    <button class="cart-btn cart-decrease">-</button>
                                    <input type="number" class="cart-quantity" value="1" min="1" max="${book.stock > 0 ? book.stock : 100}">
                                    <button class="cart-btn cart-increase">+</button>
                                    <button class="add-to-cart-btn" data-isbn="${book.isbn}">Add to Cart</button>
                                </div>
                            </div>
                        </div>
                    `;
                });
            }

            // Prepare request form HTML - make sure IDs match those expected in addbookrequest.js
            const requestFormHTML = `
                <div class="request-book-section">
                    <h3>Didn't find the book you're searching for? Chill!</h3>
                    <p>Just let us know the details, and we'll get it for you!</p>
                    <form id="bookRequestForm" class="book-request-form">
                        <input type="text" id="isbn" placeholder="ISBN (if known)" class="request-input">
                        <input type="text" id="booktitle" placeholder="Book Title" class="request-input" value="${type === 'title' ? query : ''}">
                        <input type="text" id="bookauthor" placeholder="Author" class="request-input" value="${type === 'author' ? query : ''}">
                        <input type="text" id="Book_Publisher" placeholder="Publisher (if known)" class="request-input">
                        <input type="number" id="num_required" placeholder="Quantity Needed" min="1" value="1" class="request-input">
                        <button type="submit" id="addBookRequestBtn" class="request-btn" onclick="AddBookRequest()">Request This Book</button>
                    </form>
                </div>
            `;

            // Combine book cards and request form - ALWAYS include the request form
            resultContainer.innerHTML = booksHTML + requestFormHTML;

            // Attach event listeners to each book-card's controls (only if books were found)
            if (booksArray.length > 0) {
                document.querySelectorAll('.book-card').forEach(card => {
                    const isbn = card.querySelector('.add-to-cart-btn').getAttribute('data-isbn');
                    const quantityInput = card.querySelector('.cart-quantity');

                    card.querySelector('.cart-increase').addEventListener('click', () => {
                        let value = parseInt(quantityInput.value) + 1;
                        const max = parseInt(quantityInput.getAttribute('max'));
                        quantityInput.value = Math.min(value, max);
                    });

                    card.querySelector('.cart-decrease').addEventListener('click', () => {
                        let value = parseInt(quantityInput.value) - 1;
                        quantityInput.value = Math.max(value, 1);
                    });

                    card.querySelector('.add-to-cart-btn').addEventListener('click', () => {
                        const quantity = parseInt(quantityInput.value);
                        // Check if addToCart function is available from cart.js
                        if (typeof addToCart === 'function') {
                            addToCart(isbn, quantity);
                        } else {
                            console.error("addToCart function not found. Make sure cart.js is loaded.");
                            alert("Unable to add to cart: cart functionality not available.");
                        }
                    });
                });
            }

            // Add event listener to the dynamically created book request form
            const bookRequestForm = document.getElementById('bookRequestForm');
            if (bookRequestForm) {
                bookRequestForm.addEventListener('submit', async function(event) {
                    event.preventDefault();
                    
                    try {
                        const isbn = document.getElementById('isbn')?.value.trim() || "";
                        const title = document.getElementById('booktitle')?.value.trim() || "";  // Match backend field name
                        const author = document.getElementById('bookauthor')?.value.trim() || "";  // Match backend field name
                        const publisher = document.getElementById('Book_Publisher')?.value.trim() || "";  // Match backend field name
                        const num_required = document.getElementById('num_required')?.value.trim() || "";

                        if (!title || !author || !publisher || !num_required) {
                            alert("⚠️ Please fill in all fields before submitting.");
                            return;
                        }
                        
                        if(num_required <= 0) {
                            alert("Required stock can't be negative...");
                            return;
                        }

                        // Use the field names expected by the backend
                        const data = {
                            isbn,
                            title,         // Changed from booktitle to title
                            author,        // Changed from bookauthor to author
                            publisher,     // Changed from Book_Publisher to publisher
                            num_required,
                            request_id: 'REQ_' + Date.now().toString() // Generate a unique request ID
                        };

                        const response = await fetch(`http://127.0.0.1:5000/add_book_request`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(data)
                        });

                        const result = await response.json();
                        console.log(result.message);
                        alert(result.message);
                    } 
                    catch (error) {
                        console.error("Failed to add the book request", error);
                        alert(`Failed to add the book request: ${error.message}`);
                    }
                });
            }
        } catch (error) {
            console.error("Error fetching book data:", error);
            console.error("Error details:", error.stack);
            resultContainer.innerHTML = `<p>Error searching for books: ${error.message}</p>`;
        }
    }

    // Search by Title
    document.getElementById("SearchByTitleBtn").addEventListener("click", () => {
        const query = document.getElementById("SearchByTitle").value.trim();
        searchBooks(query, "title");
    });

    // Search by Author
    document.getElementById("SearchByAuthorBtn").addEventListener("click", () => {
        const query = document.getElementById("SearchByAuthor").value.trim();
        searchBooks(query, "author");
    });

    // Add keyboard event listeners for Enter key
    document.getElementById("SearchByTitle").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            document.getElementById("SearchByTitleBtn").click();
        }
    });
    
    document.getElementById("SearchByAuthor").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            document.getElementById("SearchByAuthorBtn").click();
        }
    });
});