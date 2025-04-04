//MAK

/*async function updateStock() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/update_book_stock`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const updatedstockresult = document.getElementById('UpdatedStockResult');
        updatedstockresult.innerHTML = `
        <hr>
        <div class="request-item">
            <p>${data.message}</p>
        </div>
        </hr>`;
    }
    catch (error) {
        console.error("Failed to update stock:", error);
        alert("Failed to update the stock.");
    }
}*/

document.addEventListener("DOMContentLoaded", () => document.getElementById('stockForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await addStock();  // Call the function

    document.getElementById('addStockBtn').addEventListener('click', addStock)
}))


async function addStock(){
    try {
        // ✅ Trim values and validate
        const arrival_date = document.getElementById('arrival_date')?.value.trim() || "";
        const quantity_arrived = document.getElementById('quantity_arrived')?.value.trim() || "";
        const isbn = document.getElementById('isbn')?.value.trim() || "";
        const title= document.getElementById('title')?.value.trim() || "";
        const author = document.getElementById('author')?.value.trim() || "";
        const stockpublisher = document.getElementById('stockpublisher')?.value.trim() || "";
        const price = document.getElementById('price')?.value.trim() || "";
        const image_url = document.getElementById('image_url')?.value.trim() || "";

        if (!arrival_date || !quantity_arrived || !isbn || !stockpublisher || !title || !author || !price||!image_url) {
            alert("⚠️ Please fill in all fields before submitting.");
            return; // ✅ Stop function if any field is empty
        }
        if(price<0)
        {
            alert("Price can't be negative...");
            return;
        }
        if(quantity_arrived<=0)
        {
            alert("Quantity arrived must be positive integer...");
            return;
        }
        const today = new Date();  // Get today's date
        console.log(today);

        const arrivalDate = new Date(arrival_date);  // Convert input to Date object
        console.log("Arrival Date:", arrivalDate);

        if (arrivalDate > today) {
            console.log("📅 The date is in the future.");
            alert("📅 The date is in the future.");
            return;
        }

        const userConfirmed = confirm("Are you sure you want to add this stock?");
        if (!userConfirmed) {
            alert("Action cancelled.");
            return;  // ⛔ Stop execution if user clicks "Cancel"
        }

        const data = {
            arrival_date,
            quantity_arrived,
            isbn,
            title,
            author,
            stockpublisher,
            price,
            image_url
        };

        const response = await fetch('http://127.0.0.1:5000/add_new_entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result);

        const resultContainer = document.getElementById('AddToStoreResult');
        if (resultContainer) {
            resultContainer.innerHTML = `<p>${result.message}</p>`;
        }
    }
    catch (error) {
        console.error("Failed to add the book to store:", error);
        alert("Failed to add the book to store.");
    }
};

// ✅ Function to view existing book stock
async function viewStock() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_book_stock`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const BookStockResult = document.getElementById('BookStockResult');
        if (data.books && data.books.length > 0) {
            BookStockResult.innerHTML = data.books.map(item => {
                const formattedDate = item.arrival_date ? new Date(item.arrival_date).toDateString() : "N/A";
                console.log(formattedDate);

                // Check if stock is yet to be updated
                const updateMessage = item.flag === 1 ? `<p style="color: red; font-weight: bold;">This stock is yet to be updated</p>` : '';
                const imageHtml = item.image_url ? 
                    `<div class="book-image"><img src="${item.image_url}" alt="${item.title}" style="max-width: 100px; max-height: 150px;" /></div>` : 
                    `<div class="book-image"><p>No image available</p></div>`;
                return `
                <hr>
                <div class="request-item" style="display: flex; gap: 15px;>
                    ${imageHtml}
                    <p>ISBN: ${item.isbn}</p>
                    <p>Title: ${item.title}</p>
                    <p>Quantity_Arrived: ${item.quantity_arrived}</p>
                    <p>Arrival_Date: ${formattedDate}</p>
                    ${updateMessage}
                     
                </div>
                </hr>
            `;
            }).join('');
        } else {
            BookStockResult.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            </hr>`;
        }
    } 
    catch (error) {
        console.error("Failed to fetch stock:", error);
        alert("Failed to display book stock.");
    }
}


document.addEventListener("DOMContentLoaded", () => document.getElementById('deleteStoreForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await deleteFromStore();  // Call the function

    document.getElementById('deleteFromStoreBtn').addEventListener('click', deleteFromStore)

    
}))


async function deleteFromStore(){
    const storeisbn = document.getElementById('Storeisbn').value;
    const storeArrival=document.getElementById('StoreArrivalDate').value;
    try {

        if (!storeisbn || !storeArrival) {
            alert("⚠️ Please fill in all fields before submitting.");
            return; // ✅ Stop function if any field is empty
        }
        //const userConfirmed = confirm("Are you sure you want to delete this stock?");
        /*if (!userConfirmed) {
            alert("Action cancelled.");
            return;  // ⛔ Stop execution if user clicks "Cancel"
        }*/
        
        const response = await fetch(`http://127.0.0.1:5000/delete_from_Store/${storeisbn}/${storeArrival}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const DeleteStoreResults = document.getElementById('DeleteStoreResults');

        DeleteStoreResults.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            </hr>`
    }

    catch (error) {
        console.error("Failed to delete the book from Store", error);
        alert("Failed to delete the book from Store.");
    }
};

module.exports={
    addStock,
    viewStock,
    deleteFromStore
}


