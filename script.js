document.getElementById('footprintForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevents form submission

    // Get user inputs
    const milesDriven = parseFloat(document.getElementById('milesDriven').value);
    const dietType = document.getElementById('dietType').value;
    const energyUsage = parseFloat(document.getElementById('energyUsage').value);

    // Calculate carbon footprint
    const footprint = calculateCarbonFootprint(milesDriven, dietType, energyUsage);

    // Display the result
    document.getElementById('result').textContent = `Your estimated carbon footprint is ${footprint.toFixed(2)} kg CO2 per month.`;
});

function calculateCarbonFootprint(miles, diet, energy) {
    let dietFactor;
    
    // Assign a diet factor based on the user's diet type
    switch (diet) {
        case 'meat':
            dietFactor = 150;
            break;
        case 'vegetarian':
            dietFactor = 100;
            break;
        case 'vegan':
            dietFactor = 70;
            break;
    }

    // Example calculations for carbon emissions (simplified):
    // - Each mile driven emits approximately 0.4 kg of CO2
    // - Diet type emits different amounts of CO2 per month (dummy numbers)
    // - Energy usage emits 0.5 kg CO2 per kWh (can adjust this based on real data)

    const drivingFootprint = miles * 0.4 * 30;  // Assume 30 days in a month
    const dietFootprint = dietFactor;
    const energyFootprint = energy * 0.5;

    // Total carbon footprint (in kg CO2 per month)
    return drivingFootprint + dietFootprint + energyFootprint;
}
