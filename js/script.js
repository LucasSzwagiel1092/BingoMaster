// script.js

async function calculateBingo() {
    // Collect input values from the form
    const itemName = document.getElementById('item_name').value;
    const pointsPerGrind = parseFloat(document.getElementById('points_per_grind').value);
    const amountWanted = parseInt(document.getElementById('amount_wanted').value);
    const grindsPerHour = parseFloat(document.getElementById('grinds_per_hour').value);

    console.log("Item Name:", itemName);
    console.log("Points Per Grind:", pointsPerGrind);
    console.log("Amount Wanted:", amountWanted);
    console.log("Grinds Per Hour:", grindsPerHour);

    // Validate input
    if (
        isNaN(pointsPerGrind) ||
        isNaN(amountWanted) ||
        isNaN(grindsPerHour) ||
        itemName.trim() === ""
    ) {
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
        const response = await fetch('https://02c6-142-198-116-33.ngrok-free.app/api/calculate', {
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
        console.log(result);  // Inspect the returned result
        displayResults(result, itemName, amountWanted);  // Pass itemName and amountWanted here
    } catch (error) {
        displayError("An error occurred while fetching the data: " + error.message);
    }
}

function displayResults(result, itemName, amountWanted) {
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
        // Iterate through each result and display it correctly
        result.forEach(res => {
            const resultItem = document.createElement('li');
            if (res.error) {
                resultItem.innerHTML = `${res.monster} - Drop Chance: ${res.drop_chance} - ${res.error}`;
            } else {
                resultItem.innerHTML = `Grinding for ${amountWanted} of ${itemName} from ${res.monster} at a ${res.drop_chance} drop chance. <br> Points per hour: ${res.points_per_hour}`;
            }
            resultsList.appendChild(resultItem);
        });
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
