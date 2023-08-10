document.addEventListener("DOMContentLoaded", () => {
    const addDataBtn = document.getElementById("addDataBtn");
    const outputDiv = document.getElementById("output");

    addDataBtn.addEventListener("click", async () => {
        try {
            const response = await fetch("add_data.php"); // Change to the actual endpoint
            const result = await response.text();
            outputDiv.innerHTML = result;
        } catch (error) {
            console.error("Error adding data:", error);
            outputDiv.innerHTML = "Error adding data to the blockchain file.";
        }
    });
});
