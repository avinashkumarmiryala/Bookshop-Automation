const { fireEvent, screen } = require("@testing-library/dom");
require("@testing-library/jest-dom");

// Mock fetch globally
global.fetch = jest.fn();
global.alert = jest.fn();
global.confirm = jest.fn();

// Import the script to test
const { viewStatistics } = require("./static/statistics.js"); // Ensure correct path

describe("viewStatistics Function", () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <form id="isbnForm">
                <input type="date" id="StartDate" />
                <input type="date" id="EndDate" />
                <input type="text" id="bookisbn" />
                <button id="statBtn" type="submit">Submit</button>
            </form>
            <div id="StatContainer"></div>
        `;

        // Re-mock window.alert
        window.alert = jest.fn();
    });

    afterEach(() => {
        jest.clearAllMocks(); // Clear mocks between tests
    });

    test("alerts if fields are empty", async () => {
        // Ensure all fields are empty
        document.getElementById("StartDate").value = "";
        document.getElementById("EndDate").value = "";
        document.getElementById("bookisbn").value = "";

        await viewStatistics(); // Call the function manually

        expect(window.alert).toHaveBeenCalledWith("⚠️ Please fill in all fields before submitting.");
    });
});
