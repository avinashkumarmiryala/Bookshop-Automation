// Add this before your tests
beforeAll(() => {
    global.alert = jest.fn();  // Mock window.alert
});

afterEach(() => {
    jest.clearAllMocks();  // Clear mocks between tests
});

test("should handle fetch failure in makeRequest", async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error("Fetch failed"));

    await makeRequest();

    expect(global.alert).toHaveBeenCalledWith("Failed to fetch vendors.");
});

test("should handle fetch failure in viewRequests", async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error("Fetch failed"));

    await viewRequests();

    expect(global.alert).toHaveBeenCalledWith("Failed to display book requests.");
});





const { viewRequests,makeRequest } = require("./static/bookrequest.js");

// Mock fetch API
global.fetch = jest.fn();

describe("makeRequest function", () => {
    beforeEach(() => {
        document.body.innerHTML = '<div id="RequestVendorContainer"></div>';
        fetch.mockClear();
    });

    it("should display vendor details when response contains data", async () => {
        fetch.mockResolvedValue({
            json: jest.fn().mockResolvedValue({
                customer_name_requests: [
                    {
                        publisher: "O'Reilly",
                        vendor_details: {
                            vendor_name: "John Vendor",
                            vendor_id: "V123",
                            contact_info: "123-456-7890",
                            vendor_address: "123 Vendor St"
                        }
                    }
                ],
                book_requests: []
            })
        });

        await makeRequest();
        expect(document.getElementById("RequestVendorContainer").innerHTML).toContain("John Vendor");
    });

    it("should handle empty request data", async () => {
        fetch.mockResolvedValue({ json: jest.fn().mockResolvedValue({}) });
        await makeRequest();
        expect(document.getElementById("RequestVendorContainer").innerHTML).toContain("No book requests found.");
    });

    it("should handle fetch failure", async () => {
        fetch.mockRejectedValue(new Error("Fetch failed"));
        await makeRequest();
        expect(alert).toHaveBeenCalledWith("Failed to fetch vendors.");
    });
});

describe("viewRequests function", () => {
    beforeEach(() => {
        document.body.innerHTML = '<div id="BookRequestResult"></div>';
        fetch.mockClear();
    });

    it("should display book requests correctly", async () => {
        fetch.mockResolvedValue({
            json: jest.fn().mockResolvedValue({
                requests: [
                    {
                        request_id: 1,
                        isbn: "12345",
                        title: "JS Basics",
                        num_required: 5
                    }
                ]
            })
        });

        await viewRequests();
        expect(document.getElementById("BookRequestResult").innerHTML).toContain("JS Basics");
    });

    it("should display message if no requests found", async () => {
        fetch.mockResolvedValue({ json: jest.fn().mockResolvedValue({ message: "No requests found" }) });
        await viewRequests();
        expect(document.getElementById("BookRequestResult").innerHTML).toContain("No requests found");
    });

    it("should handle fetch failure", async () => {
        fetch.mockRejectedValue(new Error("Fetch failed"));
        await viewRequests();
        expect(alert).toHaveBeenCalledWith("Failed to display book requests.");
    });
});
