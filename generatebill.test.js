// Import necessary testing utilities

// Mock global fetch and alert
global.fetch = jest.fn();
global.alert = jest.fn();

// Create a more controlled mock for window.location
let locationHref = "";
Object.defineProperty(global, 'window', {
  value: {
    location: {
      get href() {
        return locationHref;
      },
      set href(value) {
        locationHref = value;
      }
    }
  },
  writable: true
});

const { generate_bill } = require("./static/generate_bill"); // Adjust the path

describe("generate_bill Function", () => {
    beforeEach(() => {
        jest.clearAllMocks(); // Reset mocks before each test
        // Reset location href value
        locationHref = "";
    });

    test("redirects to /generate_bill on success", async () => {
        // Mock successful fetch response
        fetch.mockResolvedValue({ ok: true });

        await generate_bill();

        expect(locationHref).toBe("/generate_bill");
    });

    test("alerts user on fetch failure", async () => {
        // Simulate a failed fetch (network error)
        fetch.mockRejectedValue(new Error("Network error"));

        await generate_bill();

        expect(alert).toHaveBeenCalledWith("Failed to generate bill. Please try again.");
    });

    test("alerts user on HTTP error response", async () => {
        // Simulate an HTTP error response (e.g., 500 Internal Server Error)
        fetch.mockResolvedValue({ ok: false, status: 500 });

        await generate_bill();

        expect(alert).toHaveBeenCalledWith("Failed to generate bill. Please try again.");
    });
});