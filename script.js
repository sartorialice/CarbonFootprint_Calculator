document.getElementById('footprintForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevents form submission

    // Get user inputs
    const milesDriven = parseFloat(document.getElementById('milesDriven').value);
    const dietType = document.getElementById('dietType').value;
    const energyUsage = parseFloat(document.getElementById('energyUsage').value);

    // Prepare the data to send
    const data = {
        miles_driven: milesDriven,
        diet_type: dietType,
        energy_usage: energyUsage
    };

    // Send data to the Flask backend
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(result => {
        // Display the result
        document.getElementById('result').textContent = `Your estimated carbon footprint is ${result.carbon_footprint.toFixed(2)} kg CO2 per month.`;
    })
    .catch(error => {
        // Display an error message
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred while calculating the carbon footprint. Please try again.';
    });
});
