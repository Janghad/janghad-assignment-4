document.getElementById('search-form').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent default form submission

    const query = document.getElementById('query').value;  // Get query from input

    // Send query to Flask backend
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })  // Send query as JSON
    });

    const resultData = await response.json();  // Parse JSON response

    // Display the results
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';  // Clear previous results

    resultData.documents.forEach((doc, index) => {
        const resultElement = document.createElement('div');
        resultElement.className = 'result';  // Add a class for styling
        resultElement.innerHTML = `
            <p><strong>Document ${resultData.indices[index]}:</strong></p>
            <p><strong>From:</strong> ${doc.author}</p>
            <p><strong>Subject:</strong> ${doc.subject}</p>
            <p><strong>Organization:</strong> ${doc.organization}</p>
            <p><strong>Content:</strong> ${doc.content}</p>
            <p><strong>Similarity:</strong> ${resultData.similarities[index].toFixed(5)}</p>
        `;
        resultsDiv.appendChild(resultElement);
    });

    // Render the similarity chart
    const ctx = document.getElementById('similarity-chart').getContext('2d');
    if (window.myChart) window.myChart.destroy();  // Clear previous chart

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: resultData.indices.map(i => `Document ${i}`),
            datasets: [{
                label: 'Cosine Similarity',
                data: resultData.similarities,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
