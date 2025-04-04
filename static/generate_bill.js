async function generate_bill() {
    try {
        const response = await fetch("http://127.0.0.1:5000/generate_bill", {
            method: "GET",
            credentials: "include"  // Include cookies/session
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Redirect to the server-rendered bill page
        window.location.href = "/generate_bill";
    } catch (error) {
        console.error("Failed to fetch bill:", error);
        alert("Failed to generate bill. Please try again.");
    }
}
module.exports={
    generate_bill
}