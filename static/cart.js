// Function to add book to cart
function addToCart(isbn, quantity) {
    console.log(`Adding to cart: ISBN=${isbn}, Quantity=${quantity}`);
    fetch('/add_to_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ isbn, quantity })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log("Add to Cart Response:", data);
        if (data.status === 'success') {
            alert(data.message); // e.g., "✅ Added 1 copies..."
        } else if (data.status === 'warning') {
            alert(data.message); // e.g., "✅ Added X copies, requested Y more"
        } else if (data.status === 'out_of_stock') {
            alert(data.message); // e.g., "⚠️ Out of stock! Request recorded"
        } else {
            alert(`Unexpected response: ${data.message || 'Unknown error'}`);
        }
        updateCartCount();
        viewCart();
    })
    .catch(err => {
        console.error('Error adding to cart:', err);
        alert('Failed to add item to cart: ' + err.message);
    });
}


// Function to update cart item (when using + or - buttons)
function updateCartItem(isbn, quantity) {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const user_id = user.username;  // Get username from login
    console.log(`Updating cart item: ISBN=${isbn}, Quantity=${quantity}, User=${user_id}`);
    
    if (!user_id) {
        alert("Please log in to update your cart!");
        window.location.href = "/login";
        return;
    }

    fetch("/update_cart_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ isbn, quantity, user_id })
    })
    .then(response => {
        console.log('Update cart response status:', response.status);
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log("Cart Updated:", data);
        alert(data.message); // Optional
        viewCart();  // Refresh cart
        updateCartCount();
    })
    .catch(error => {
        console.error("Error updating cart:", error);
        alert('Failed to update cart: ' + error.message);
    });
}


// Function to load cart items into the sticky sidebar
function viewCart() {
    console.log("Fetching cart data...");
    fetch('/view_cart')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log("Cart Data Received:", data);
            const cartContent = document.getElementById('cart-content');
            if (!cartContent) {
                console.error("Cart content element not found!");
                return;
            }
            cartContent.innerHTML = '';

            // The items array is directly in data.items
            const items = data.items;
            
            if (!items || items.length === 0) {
                cartContent.innerHTML = '<p>Your cart is empty</p>';
                cartContent.innerHTML += '<button id="generate-bill-btn">Generate Bill</button>';
                document.getElementById('generate-bill-btn').addEventListener('click', () => {
                    window.location.href = '/generate_bill';
                });
                return;
            }

            items.forEach(item => {
                cartContent.innerHTML += `
                    <div class="cart-item" data-isbn="${item.isbn}">
                        <img src="${item.image_url}" class="cart-img" style="width: 50px; height: 75px">
                        <p>${item.title} (₹${item.price}) - ISBN: ${item.isbn}</p>
                        <div class="cart-controls">
                            <button class="cart-decrease">-</button>
                            <input type="number" value="${item.quantity}" min="1" readonly>
                            <button class="cart-increase">+</button>
                        </div>
                    </div>
                `;
            });

            // Rest of the function remains the same

            cartContent.innerHTML += '<button id="generate-bill-btn">Generate Bill</button>';
            document.getElementById('generate-bill-btn').addEventListener('click', () => {
                window.location.href = '/generate_bill';
            });

            // Attach event listeners for cart controls
            document.querySelectorAll('.cart-decrease').forEach(button => {
                button.addEventListener('click', function () {
                    const parent = this.closest(".cart-item");
                    const input = parent.querySelector("input");
                    let quantity = parseInt(input.value) - 1;  // Allow it to go to 0 or below
                    if (quantity <= 0) {
                        quantity = 0;  // Set to 0 to trigger removal
                    }
                    input.value = quantity;
                    const isbn = parent.getAttribute("data-isbn");
                    updateCartItem(isbn, quantity);
                    if (quantity === 0) {
                        viewCart();  // Refresh cart to remove the item visually
                    }
                });
            });

            document.querySelectorAll('.cart-increase').forEach(button => {
                button.addEventListener('click', function () {
                    const parent = this.closest(".cart-item");
                    const input = parent.querySelector("input");
                    let quantity = parseInt(input.value) + 1;
                    input.value = quantity;
                    const isbn = parent.getAttribute("data-isbn");
                    updateCartItem(isbn, quantity);
                });
            });
        })
        .catch(error => {
            console.error("Error loading cart:", error);
            cartContent.innerHTML = '<p>Error loading cart: ' + error.message + '</p>';
        });
}


function updateCartCount() {
    console.log("Updating cart count...");
    fetch('/view_cart')
        .then(response => response.json())
        .then(data => {
            console.log("Cart Count Data:", data);
            const cartCountElement = document.getElementById('cart-count');
            if (!cartCountElement) return;
            const itemCount = (data.status === 'success' && data.items) 
                ? data.items.reduce((sum, item) => sum + (item.quantity || 0), 0) 
                : 0;
            cartCountElement.textContent = itemCount.toString();
        })
        .catch(error => console.error("Error updating cart count:", error));
}

    document.querySelectorAll('.cart-decrease').forEach(button => {
        button.addEventListener('click', function () {
            const parent = this.closest(".cart-item");
            const input = parent.querySelector("input");
            let quantity = Math.max(parseInt(input.value) - 1, 1);
            input.value = quantity;

            const isbn = parent.getAttribute("data-isbn");
            console.log(`Decreasing quantity for ISBN=${isbn} to ${quantity}`);
            updateCartItem(isbn, quantity);
        });
    });


// Function to update cart count indicator


// Initialize cart functionality
document.addEventListener('DOMContentLoaded', function () {
    updateCartCount(); // Update cart count on load

    // Open cart sidebar on click
    const cartIcon = document.getElementById("cart-icon");
    if (cartIcon) {
        cartIcon.addEventListener("click", function () {
            console.log("Cart icon clicked, opening sidebar...");
            const sidebar = document.getElementById("cart-sidebar");
            sidebar.classList.add("open");
            viewCart(); // Load cart items in sidebar
        });
    } else {
        console.error("Cart icon not found!");
    }

    // Close cart sidebar
    const closeCartBtn = document.getElementById("close-cart");
    if (closeCartBtn) {
        closeCartBtn.addEventListener("click", function () {
            console.log("Closing cart sidebar...");
            document.getElementById("cart-sidebar").classList.remove("open");
        });
    } else {
        console.error("Close cart button not found!");
    }

    // If we're on the cart page, load cart items (optional, since we’re using sidebar)
    if (document.getElementById('cart-items')) {
        viewCart();
    }

    // Setup generate bill button
    const generateBillBtn = document.getElementById('generate-bill-btn');
    if (generateBillBtn) {
        generateBillBtn.addEventListener('click', function () {
            console.log("Generating bill...");
            fetch('/generate_bill')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const cartContent = document.getElementById('cart-content');
                        cartContent.innerHTML = `
                            <h3>Receipt</h3>
                            <p>Transaction ID: ${data.transaction_id}</p>
                            <p>Date: ${data.date}</p>
                            <ul>
                                ${data.items.map(item => `<li>${item.title} - ${item.quantity} x INR${item.price} = INR${item.subtotal}</li>`).join('')}
                            </ul>
                            <p>Total: INR${data.total_amount}</p>
                        `;
                        updateCartCount(); // Reset count after billing
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error("Error generating bill:", error));
        });
    }
});


module.exports={
    addToCart, updateCartItem, viewCart, updateCartCount
}