//MAK
async function viewVendors() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_all_vendors`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const GetVendorResults = document.getElementById('GetVendorResults');
        if (Array.isArray(data.message)) {
            GetVendorResults.innerHTML = `
                <div class="vendor-result-wrapper">
                    ${data.message.map(item => `
                        <div class="vendor">
                            <div class="spring-dots">
                                ${Array(5).fill().map(() => `<span class="dot"></span>`).join('')}
                            </div>
                            <div class="vendor-result">
                                <p><strong>Vendor ID:</strong> ${item.vendor_id}</p>
                                <p><strong>Vendor Name:</strong> ${item.vendor_name}</p>
                                <p><strong>Vendor Address:</strong> ${item.vendor_address}</p>
                                <p><strong>Contact INFO:</strong> ${item.contact_info}</p>
                                <p><strong>Publisher:</strong> ${item.publisher}</p>
                            </div>
                        </div>
                        <hr>
                    `).join('')}
                </div>
            `;
        }
        else {
            GetVendorResults.innerHTML = `<p>${data.message}</p>`;
        }
    }
    catch (error) {
        console.error("Failed to fetch book vendors:", error);
        alert("Failed to display book vendors.");
    }
};



document.addEventListener("DOMContentLoaded", () => document.getElementById('vendorForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await addVendor();  // Call the function


    document.getElementById('addVendorBtn').addEventListener('click', addVendor)}
))


async function addVendor(){
    try {
        // ✅ Trim values and validate
        const vendor_name = document.getElementById('vendor_name')?.value.trim() || "";
        const vendor_address = document.getElementById('vendor_address')?.value.trim() || "";
        const contact_info = document.getElementById('contact_info')?.value.trim() || "";
        const publisher = document.getElementById('publisher')?.value.trim() || "";

        console.log(vendor_name, vendor_address, contact_info, publisher); // ✅ Debug values

        if (!vendor_name || !vendor_address || !contact_info || !publisher) {
            alert("⚠️ Please fill in all fields before submitting.");
            return; // ✅ Stop function if any field is empty
        }

        /*const userConfirmed = confirm("Are you sure you want to add this vendor?");
        if (!userConfirmed) {
            alert("Action cancelled.");
            return;  // ⛔ Stop execution if user clicks "Cancel"
        }*/

        const data = {
            vendor_name,
            vendor_address,
            contact_info,
            publisher
        };

        const response = await fetch('http://127.0.0.1:5000/add_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result);

        const resultContainer = document.getElementById('AddToVendorResult');
        if (resultContainer) {
            resultContainer.innerHTML = `<p>${result.message}</p>`;
        }
    }
    catch (error) {
        console.error("Failed to add the Vendor.", error);
        alert("Failed to add the Vendor.");
    }
};


document.addEventListener("DOMContentLoaded", () => document.getElementById('vendorForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await deleteVendor();  // Call the function
    document.getElementById('deleteVendorBtn').addEventListener('click', deleteVendor)
    
}))

async function deleteVendor(){
    const bookpublisher = document.getElementById('BookPublisher').value;
    try {

        if (!bookpublisher) {
            alert("⚠️ Please fill in all fields before submitting.");
            return; // ✅ Stop function if any field is empty
        }
        /*const userConfirmed = confirm("Are you sure you want to delete this vendor?");
        if (!userConfirmed) {
            alert("Action cancelled.");
            return;  // ⛔ Stop execution if user clicks "Cancel"
        }*/
        
        const response = await fetch(`http://127.0.0.1:5000/delete_from_Vendor_Supply/${bookpublisher}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const DeleteVendorResults = document.getElementById('DeleteVendorResults');

        DeleteVendorResults.innerHTML = `
            <hr>
            <div class="request-item">
                <p>${data.message}</p>
            </div>
            </hr>`
    }

    catch (error) {
        console.error("Failed to delete book vendors:", error);
        alert("Failed to delete book vendors.");
    }
};

module.exports={
    deleteVendor,
    addVendor,
    viewVendors
}