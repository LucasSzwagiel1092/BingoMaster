document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'https://random-name.ngrok.io/api/data';  // Replace with your ngrok URL
  
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Data from backend:', data);
        // Use the data to update your webpage, e.g., dynamically populate elements
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  });
  