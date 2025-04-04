//MAK
document.addEventListener("DOMContentLoaded", () => {document.getElementById('isbnForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // ✅ Prevent default form submission

    await viewStatistics();  // Call the function

    document.getElementById('statBtn').addEventListener('click', viewStatistics)}

)});


async function viewStatistics()
{
    const strt = document.getElementById('StartDate')?.value.trim() || "";;
    const end = document.getElementById('EndDate')?.value.trim() || "";;
    const bookisbn = document.getElementById('bookisbn')?.value.trim() || "";
    if (!strt || !end || !bookisbn) {
        alert("⚠️ Please fill in all fields before submitting.");
        return; // ✅ Stop function if any field is empty
    }
    const today = new Date();  // Get today's date
    const strtDate = new Date(strt);  // Convert input to Date object
    const endDate = new Date(end);
    if (strtDate > today) {
        console.log("📅 The start date is in the future.");
        alert("📅 The start date is in the future. Not Possible!");
        return;
    }
    if(strtDate > endDate){
        console.log("📅 The End Date is prior to the Start Date.");
        alert("📅 The end date is prior to the start Date. Not Possible!");
        return;
    }
    
    const response = await fetch(`http://127.0.0.1:5000/transactions_statistics/${bookisbn}/${strt}/${end}`);

    const data = await response.json();

    // Display Stats dynamically
    const StatContainer = document.getElementById('StatContainer');
    
    if(data.message){
        StatContainer.innerHTML = `
        <hr>
        <div class="request-item">
            <p>${data.message}</p>
        </div>
        <hr>
        `;
    }
    else{
        StatContainer.innerHTML = `
        <hr>
        <div class="request-item">
            <p>ISBN: ${data.isbn}</p>
            <p>Total Sold: ${data.total_sold}</p>
        </div>
        <hr>
        `;
    }
};

module.exports={
    viewStatistics
}

