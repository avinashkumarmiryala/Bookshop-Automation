//MAK

async function viewBooks() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_all_books`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const GetBookResults = document.getElementById('GetBookResults');
        if (Array.isArray(data.message)) {
            GetBookResults.innerHTML = data.message.map(item => {
                const formattedDate = item.request_date ? new Date(item.request_date).toDateString() : "N/A";
                console.log(formattedDate); 
                const imageHtml = item.image_url ? 
                    `<div class="book-image"><img src="${item.image_url}" alt="${item.title}" style="max-width: 100px; max-height: 150px;" /></div>` : 
                    `<div class="book-image"><p>No image available</p></div>`;
                return `
                <hr>
                <div class="request-item" style="display: flex; gap: 15px;>
                     ${imageHtml}
                    <p>ISBN: ${item.isbn}</p>
                    <p>Title: ${item.title}</p>
                    <p>Author: ${item.author}</p>
                    <p>Publisher: ${item.publisher}</p>
                    <p>Price: ${item.price}</p>
                    <p>Stock: ${item.stock}</p>
                    <p>Rack: ${item.rack}</p>
                    <p>Required Copies: ${item.num_required}</p>
                    <p>Request Date: ${formattedDate}</p>
                    <p>Average: ${item.average}</p>
                </div>
                <hr>`;
            }).join('');
        } else {
            GetBookResults.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            <hr>`;
        }
    }
    catch (error) {
        console.error("Failed to fetch books:", error);
        alert("Failed to display books.");
    }
};



document.addEventListener("DOMContentLoaded", () => {document.getElementById('deleteBookForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await deleteBook();  // Call the function

    document.getElementById('deleteBookBtn').addEventListener('click', deleteBook);
})})

async function deleteBook(){
    const deleteisbn = document.getElementById('Deleteisbn').value;
    try {

        if (!deleteisbn) {
            alert("⚠️ Please fill in all fields before submitting.");
            return; // ✅ Stop function if any field is empty
        }

        const userConfirmed = confirm("Are you sure you want to delete this book?");
        if (!userConfirmed) {
            alert("Action cancelled.");
            return;  // ⛔ Stop execution if user clicks "Cancel"
        }
        
        const response = await fetch(`http://127.0.0.1:5000/delete_from_Book/${deleteisbn}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const DeleteBookResults = document.getElementById('DeleteBookResults');

        DeleteBookResults.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            </hr>`
    }

    catch (error) {
        console.error("Failed to delete the book:", error);
        alert("Failed to delete the book.");
    }
};


document.addEventListener("DOMContentLoaded", () => {document.getElementById('editBookForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await editPrice();  // Call the function
    document.getElementById('UpdatePriceBtn').addEventListener('click', editPrice);

})})

async function editPrice() {

    const editisbn = document.getElementById('Editisbn')?.value.trim() || "";
    const newPrice = document.getElementById('newPrice')?.value.trim() || "";

    if (!editisbn || !newPrice ) {
        alert("⚠️ Please fill in all fields before submitting.");
        return; // ✅ Stop function if any field is empty
    }

    if (isNaN(newPrice) || newPrice <= 0) {
        alert("❌ Invalid price! Enter a valid positive number.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/update_price/${editisbn}/${newPrice}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            //body: JSON.stringify({ price: parseFloat(newPrice) })
        });

        const data = await response.json();
        console.log("Response from server:", data);
        const priceResult = document.getElementById('PriceResult');

        priceResult.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            </hr>`
    } catch (error) {
        console.error("Error updating price:", error);
        alert("❌ Failed to update price. Try again.");
    }
}
async function displayBooksGrid() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_all_books`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server for grid display:", data);

        const GetBookResults = document.getElementById('GetBookResults');
        GetBookResults.innerHTML = '<h2>All Books</h2>';
        
        if (Array.isArray(data.message)) {
            // Create a grid container
            const bookGrid = document.createElement('div');
            bookGrid.className = 'books-grid';
            
            // Process each book
            data.message.forEach(item => {
                const formattedDate = item.request_date ? new Date(item.request_date).toDateString() : "N/A";
                const imageUrl = item.image_url || 'https://via.placeholder.com/150x200?text=No+Image';
                
                // Create book card
                const bookCard = document.createElement('div');
                bookCard.className = 'book-card';
                
                bookCard.innerHTML = `
                    <div class="book-image">
                        <img src="${imageUrl}" alt="${item.title}" onerror="this.src='https://via.placeholder.com/150x200?text=No+Image'">
                    </div>
                    <div class="book-details">
                        <h3>${item.title || 'Unknown Title'}</h3>
                        <p class="author">by ${item.author || 'Unknown Author'}</p>
                        <p class="isbn">ISBN: ${item.isbn || 'N/A'}</p>
                        <p class="publisher">Publisher: ${item.publisher || 'N/A'}</p>
                        <p class="price">Price: ₹${item.price || 'N/A'}</p>
                        <p class="stock">In Stock: ${item.stock || '0'}</p>
                        <p class="rack">Rack: ${item.rack || 'N/A'}</p>
                    </div>
                `;
                
                bookGrid.appendChild(bookCard);
            });
            
            GetBookResults.appendChild(bookGrid);
        } else {
            GetBookResults.innerHTML += `
            <div class="no-books-message">
                <p>${data.message}</p>
            </div>`;
        }
    }
    catch (error) {
        console.error("Failed to display books in grid:", error);
        const GetBookResults = document.getElementById('GetBookResults');
        GetBookResults.innerHTML += `
        <div class="error-message">
            <p>Failed to load books in grid view. Please try again later.</p>
        </div>`;
    }
}



module.exports = {
    viewBooks,
    deleteBook,
    editPrice,
    displayBooksGrid
};