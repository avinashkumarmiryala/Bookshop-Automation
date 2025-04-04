/**
 * @jest-environment jsdom
 */

const { addStock, viewStock, deleteFromStore } = require("./static/storeops");
global.alert = jest.fn();
global.confirm = jest.fn();


global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true, // Ensures the response is considered successful
      json: () => Promise.resolve({ message: "Success" }),
    })
  );
  
  jest.spyOn(window, "alert").mockImplementation(() => {});
  jest.spyOn(window, "confirm").mockImplementation(() => true); // Mock confirmation


beforeEach(() => {
  document.body.innerHTML = `
    <form id="stockForm">
      <input id="arrival_date" value="2024-04-02" />
      <input id="quantity_arrived" value="10" />
      <input id="isbn" value="1234567890" />
      <input id="title" value="Test Book" />
      <input id="author" value="John Doe" />
      <input id="stockpublisher" value="Test Publisher" />
      <input id="price" value="100" />
      <input id="image_url" value="http://example.com/book.jpg" />
      <button id="addStockBtn"></button>
    </form>
    <div id="AddToStoreResult"></div>

    <div id="BookStockResult"></div>

    <form id="deleteStoreForm">
      <input id="Storeisbn" value="1234567890" />
      <input id="StoreArrivalDate" value="2024-04-02" />
      <button id="deleteFromStoreBtn"></button>
    </form>
    <div id="DeleteStoreResults"></div>
  `;
});

test("addStock sends a POST request and updates UI", async () => {
    console.log("Calling addStock...");
    await addStock();
    console.log("Fetch called with:", fetch.mock.calls);
  
    expect(fetch).toHaveBeenCalledWith(
      "http://127.0.0.1:5000/add_new_entry",
      expect.objectContaining({ method: "POST" })
    );
    
    // Checking that result is displayed in DOM instead of checking alert
    expect(document.getElementById("AddToStoreResult").innerHTML).toContain("Success");
  });

test("viewStock sends a GET request and updates UI", async () => {
  fetch.mockResolvedValueOnce({
    json: () => Promise.resolve({ books: [{ isbn: "1234567890", title: "Test Book", quantity_arrived: 10, arrival_date: "2024-04-02" }] }),
  });

  await viewStock();

  expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:5000/get_book_stock", expect.objectContaining({ method: "GET" }));

  expect(document.getElementById("BookStockResult").textContent).toContain("Test Book");
});

test("deleteFromStore sends DELETE request and updates UI", async () => {

    fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: "Book deleted successfully" })
    });
    await deleteFromStore();
  
    expect(fetch).toHaveBeenCalledWith(
      "http://127.0.0.1:5000/delete_from_Store/1234567890/2024-04-02",
      expect.objectContaining({ method: "DELETE" })
    );
  
    // Checking that result is displayed in DOM instead of checking alert
    expect(document.getElementById("DeleteStoreResults").innerHTML).toContain("Book deleted successfully");
  });