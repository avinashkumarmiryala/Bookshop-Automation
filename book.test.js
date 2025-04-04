// Set up a mock DOM before tests


const { viewBooks, deleteBook, editPrice } = require("./static/book.js");

global.fetch = jest.fn();
global.alert = jest.fn();
global.confirm = jest.fn();

describe("viewBooks", () => {
    beforeEach(() => {
        document.body.innerHTML = `<div id='GetBookResults'></div>`;
    });
    
    it("should fetch and display books correctly", async () => {
        fetch.mockResolvedValue({
            json: jest.fn().mockResolvedValue({ message: [{
                isbn: "12345", title: "JS Basics", author: "John Doe",
                publisher: "O'Reilly", price: 500, stock: 10,
                rack: "A1", num_required: 5, request_date: "2025-03-20",
                average: 4.5
            }] })
        });

        await viewBooks();
        expect(document.getElementById("GetBookResults").innerHTML).toContain("JS Basics");
    });

    it("should handle empty or incorrect response", async () => {
        fetch.mockResolvedValue({ json: jest.fn().mockResolvedValue({ message: "No books found" }) });
        await viewBooks();
        expect(document.getElementById("GetBookResults").innerHTML).toContain("No books found");
    });

    it("should handle fetch failure", async () => {
        fetch.mockRejectedValue(new Error("Fetch failed"));
        await viewBooks();
        expect(alert).toHaveBeenCalledWith("Failed to display books.");
    });
});

describe("deleteBook", () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <input id='Deleteisbn' value='12345'>
            <div id='DeleteBookResults'></div>
        `;
        require("./static/book.js"); // Re-import after modifying DOM
    });

    it("should alert if ISBN field is empty", async () => {
        document.getElementById("Deleteisbn").value = "";
        await deleteBook();
        expect(alert).toHaveBeenCalledWith("⚠️ Please fill in all fields before submitting.");
    });

    it("should confirm before deleting and handle successful deletion", async () => {
        confirm.mockReturnValue(true);
        fetch.mockResolvedValue({ json: jest.fn().mockResolvedValue({ message: "Book deleted successfully" }) });
        await deleteBook();
        expect(document.getElementById("DeleteBookResults").innerHTML).toContain("Book deleted successfully");
    });

    it("should handle fetch failure", async () => {
        confirm.mockReturnValue(true);
        fetch.mockRejectedValue(new Error("Delete failed"));
        await deleteBook();
        expect(alert).toHaveBeenCalledWith("Failed to delete the book.");
    });
});

describe("editPrice", () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <input id='Editisbn' value='12345'>
            <input id='newPrice' value='600'>
            <div id='PriceResult'></div>
        `;
    });

    it("should alert if any field is empty", async () => {
        document.getElementById("newPrice").value = "";
        await editPrice();
        expect(alert).toHaveBeenCalledWith("⚠️ Please fill in all fields before submitting.");
    });

    it("should alert if price is invalid", async () => {
        document.getElementById("newPrice").value = "-10";
        await editPrice();
        expect(alert).toHaveBeenCalledWith("❌ Invalid price! Enter a valid positive number.");
    });

    it("should handle successful price update", async () => {
        fetch.mockResolvedValue({ json: jest.fn().mockResolvedValue({ message: "Price updated successfully" }) });
        await editPrice();
        expect(document.getElementById("PriceResult").innerHTML).toContain("Price updated successfully");
    });

    it("should handle fetch failure", async () => {
        fetch.mockRejectedValue(new Error("Update failed"));
        await editPrice();
        expect(alert).toHaveBeenCalledWith("❌ Failed to update price. Try again.");
    });
});
