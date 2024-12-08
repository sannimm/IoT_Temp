import { useState, useEffect } from "react";
import { Chart } from "react-google-charts";
import Footer from "./Footer";
import Header from "./Header";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [limitValue, setLimitValue] = useState("");
  const [currentLimit, setCurrentLimit] = useState(null);

  // Haetaan lämpötila-data
  useEffect(() => {
    const fetchData = () => {
      fetch("https://temperatures.azurewebsites.net/get_temp")
        .then((response) => response.json())
        .then((data) => setData(data))
        .catch((error) => console.error("Error fetching data:", error));
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  // Google Chart data
  const chartData = [
    ["Timestamp", "Temperature"],
    ...data.map((item) => [
      new Date(item.TimeStamp).toLocaleString(),
      item.Temp,
    ]),
  ];

  const options = {
    title: "Temperature",
    curveType: "function",
    legend: { position: "bottom" },
    hAxis: { title: "Time" },
    vAxis: { title: "Temperature (°C)" },
  };

  // Lähetä raja-arvo
  const sendLimitValue = () => {
    const limit = parseFloat(limitValue);

    if (isNaN(limit)) {
      alert("Please enter a valid float number for the limit value.");
      return;
    }

    fetch("https://temperatures.azurewebsites.net/post_limit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ limit_value: limit }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Limit updated:", data);
        setCurrentLimit(limit);
      })
      .catch((error) => console.error("Error updating limit:", error));
  };

  console.log(data); // Onko tässä mitään sisältöä?
  console.log("Chart data:", chartData);
  return (
    <>
      <main>
        {data && (
          <Chart
            chartType="LineChart"
            width="800px"
            height="400px"
            data={chartData}
            options={options}
          />
        )}
        <div>
          <p>
            Current Limit: {currentLimit !== null ? currentLimit : "Not set"}
          </p>
          <input
            type="text"
            placeholder="Set Limit Value"
            value={limitValue}
            onChange={(e) => setLimitValue(e.target.value)}
          />
          <button onClick={sendLimitValue}>Update Limit</button>
        </div>
      </main>
    </>
  );
}

export default App;
