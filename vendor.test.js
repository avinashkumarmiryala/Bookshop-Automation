require("@testing-library/jest-dom");

global.fetch = jest.fn();
global.alert = jest.fn();
global.confirm = jest.fn();

const { addVendor, deleteVendor, viewVendors } = require('./static/vendor');

describe("Vendor Management Tests", () => {
    
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="GetVendorResults"></div>
            <div id="AddToVendorResult"></div>
            <div id="DeleteVendorResults"></div>
            <form id="vendorForm">
                <input id="vendor_name" value="Test Vendor"/>
                <input id="vendor_address" value="123 Test Street"/>
                <input id="contact_info" value="9876543210"/>
                <input id="publisher" value="Test Publisher"/>
                <input id="BookPublisher" value=""/>
                <button id="addVendorBtn"></button>
                <button id="deleteVendorBtn"></button>
            </form>
        `;
        fetch.mockClear();
    });
    

    test("viewVendors fetches and displays vendors", async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: [{ vendor_id: 1, vendor_name: "Vendor 1", vendor_address: "Address 1", contact_info: "12345", publisher: "Publisher 1" }] })
        });

        await viewVendors();

        expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:5000/get_all_vendors", { method: "GET" });
        expect(document.getElementById("GetVendorResults").innerHTML).toContain("Vendor 1");
    });

    test("addVendor submits form and updates UI", async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: "Vendor added successfully" })
        });

        await addVendor();

        expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:5000/add_details", expect.objectContaining({ method: "POST" }));
        expect(document.getElementById("AddToVendorResult").innerHTML).toContain("Vendor added successfully");
    });

    test("deleteVendor sends DELETE request and updates UI", async () => {
        document.getElementById("BookPublisher").value = "Test Publisher";

        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: "Vendor deleted successfully" })
        });

        await deleteVendor();

        expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:5000/delete_from_Vendor_Supply/Test Publisher", { method: "DELETE" });
        expect(document.getElementById("DeleteVendorResults").innerHTML).toContain("Vendor deleted successfully");
    });

});
