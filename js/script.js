// script.js

async function calculateBingo() {
    // Collect input values from the form
    const itemName = document.getElementById('item_name').value;
    const pointsPerGrind = parseFloat(document.getElementById('points_per_grind').value);
    const amountWanted = parseInt(document.getElementById('amount_wanted').value);
    const grindsPerHour = parseFloat(document.getElementById('grinds_per_hour').value);

    // Validate input
    if (isNaN(pointsPerGrind) || isNaN(amountWanted) || isNaN(grindsPerHour)) {
        displayError("Please enter valid numerical values in all fields.");
        return;
    }

    // Prepare data to send to the backend
    const data = {
        item_name: itemName,
        points_per_grind: pointsPerGrind,
        amount_wanted: amountWanted,
        grinds_per_hour: grindsPerHour
    };

    try {
        // Send data to the backend using fetch
        const response = await fetch('https://439b-142-198-116-33.ngrok-free.app/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data from backend.');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        displayError("An error occurred while fetching the data: " + error.message);
    }
}

function displayResults(result) {
    // Clear any previous error messages
    clearError();

    // Display the results
    const resultsContainer = document.getElementById('results-container');
    const resultsList = document.getElementById('results-list');

    resultsList.innerHTML = ''; // Clear previous results

    if (result.error) {
        const errorItem = document.createElement('li');
        errorItem.innerHTML = result.error;
        resultsList.appendChild(errorItem);
    } else {
        const resultItem = document.createElement('li');
        resultItem.innerHTML = `${result.message}<br> Points per hour: ${result.points_per_hour}`;
        resultsList.appendChild(resultItem);
    }

    // Show the results container
    resultsContainer.style.display = 'block';
}

function displayError(message) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.textContent = message;
    errorMessageElement.style.display = 'block';
}

function clearError() {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.textContent = '';
    errorMessageElement.style.display = 'none';
}
