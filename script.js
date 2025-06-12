function setAlert() {
    const ticker = document.getElementById("tickerInput").value.toUpperCase();
    const price = parseFloat(document.getElementById("priceInput").value);
  
    fetch("/set-alert", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ ticker: ticker, target: price })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("response").textContent = data.message;
    })
    .catch(err => {
      document.getElementById("response").textContent = "Error sending alert.";
      console.error(err);
    });
  }
  