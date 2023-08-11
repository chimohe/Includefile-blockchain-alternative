<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockchain Data Entry</title>
</head>
<body>
    <h1>Blockchain Data Entry</h1>
    <form id="blockchain-form">
        <!-- Dynamic block creation using JavaScript -->
    </form>
    <button id="add-block">Add Block</button>
    <button id="submit-form">Submit</button>

    <script>
        const form = document.getElementById('blockchain-form');
        const addBlockButton = document.getElementById('add-block');
        const submitButton = document.getElementById('submit-form');
        let blockCount = 0;

        addBlockButton.addEventListener('click', () => {
            blockCount++;
            const blockDiv = document.createElement('div');
            blockDiv.innerHTML = `
                <h2>Block ${blockCount}</h2>
                <textarea name="block${blockCount}_data" rows="4" cols="50" placeholder="Enter Block ${blockCount} data"></textarea>
                <br>
                <input type="file" name="file_block${blockCount}">
                <br>`;
            form.insertBefore(blockDiv, addBlockButton);
        });

        submitButton.addEventListener('click', async () => {
            const formData = new FormData(form);
            try {
                const response = await fetch('process_form.php', {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    alert('Data submitted successfully');
                } else {
                    alert('Error submitting data');
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        });
    </script>
</body>
</html>
