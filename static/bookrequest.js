//MAK

async function makeRequest() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/make_requests`, {
            method: "GET"
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const RequestVendorContainer = document.getElementById('RequestVendorContainer');

        if (data.customer_name_requests || data.book_requests) {
            let output = '<hr>'
            output +=  '<div class="request-item">'; // Start of the container;

            // Handle customer_name_requests
            if (data.customer_name_requests) {
                output += data.customer_name_requests.map(item => `
                    <p>Publisher: ${item.publisher}</p>
                    ${item.vendor_details ? `
                        <p>Vendor Name: ${item.vendor_details.vendor_name}</p>
                        <p>Vendor ID: ${item.vendor_details.vendor_id}</p>
                        <p>Contact INFO: ${item.vendor_details.contact_info}</p>
                        <p>Vendor Address: ${item.vendor_details.vendor_address}</p>
                        <br>
                    ` : `<p>${item.message}</p>
                        <br>`}
                `).join('');
            }

            // Handle book_requests
            if (data.book_requests) {
                output += data.book_requests.map(item => `
                    <p>Publisher: ${item.publisher}</p>
                    ${item.vendor_details ? `
                        <p>Vendor Name: ${item.vendor_details.vendor_name}</p>
                        <p>Vendor ID: ${item.vendor_details.vendor_id}</p>
                        <p>Contact INFO: ${item.vendor_details.contact_info}</p>
                        <p>Vendor Address: ${item.vendor_details.vendor_address}</p>
                        <br>
                    ` : `<p>${item.message}</p>
                        <br>`}
                `).join('');
            }
            
            output += '</div>'; // End of the container

            output+='<hr>';

            RequestVendorContainer.innerHTML = output;
        } else {
            RequestVendorContainer.innerHTML = `<p>No book requests found.</p>`;
        }
    } 
    catch (error) {
        console.error("Failed to fetch vendors", error);
        alert("Failed to fetch vendors.");
    }
}


async function viewRequests(){
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_all_requests`, {
            method: 'GET'
        });
        const data = await response.json();

        console.log("Response from server:", data);

        const BookRequestResult = document.getElementById('BookRequestResult');
        if (Array.isArray(data.requests)) {
            BookRequestResult.innerHTML = data.requests.map(item => `
                <hr>
                <div class="request-item">
                    <p>Request_id: ${item.request_id}</p>
                    <p>ISBN: ${item.isbn}</p>
                    <p>Title: ${item.title}</p>
                    <p>Num_required: ${item.num_required}</p>
                    <br>
                </div>
                <hr>
            `).join('');
        } else {
            BookRequestResult.innerHTML = `<p>${data.message}</p>`;
        }
    }
    catch (error) {
        console.error("Failed to fetch book requests:", error);
        alert("Failed to display book requests.");
    }
};



module.exports = { viewRequests,makeRequest };