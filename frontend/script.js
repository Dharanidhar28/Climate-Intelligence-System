let tempChart = null;
let humidityChart = null;
let windChart = null;

let currentCity = null;

async function loadWeather() {
	currentCity = document.getElementById("city").value;

	await fetchAndUpdate(currentCity);
	await checkHeatwave(currentCity);
}

async function checkHeatwave(city) {
	const response = await fetch(`${API_BASE_URL}/heatwave/${city}`);
	const data = await response.json();

	console.log("Heatwave:", data);

	const alertBox = document.getElementById("heatwaveAlert");

	if (data.heatwave) {
		alertBox.innerHTML = "Heatwave detected!";
		alertBox.style.color = "red";
	} else {
		alertBox.innerHTML = "No heatwave";
		alertBox.style.color = "green";
	}
}

async function fetchAndUpdate(city) {
	const response = await fetch(`${API_BASE_URL}/history/${city}`);
	const data = await response.json();

	console.log(data);

	const temps = data.map((d) => d.temperature);
	const humidity = data.map((d) => d.humidity);
	const wind = data.map((d) => d.wind_speed);

	const labels = data.map((d) => new Date(d.time).toLocaleTimeString());

	if (tempChart) {
		tempChart.destroy();
	}
	if (humidityChart) {
		humidityChart.destroy();
	}
	if (windChart) {
		windChart.destroy();
	}

	tempChart = new Chart(document.getElementById("tempChart"), {
		type: "line",
		data: {
			labels: labels,
			datasets: [
				{
					label: "Temperature (°C)",
					data: temps,
					borderColor: "red",
					backgroundColor: "pink",
					tension: 0.3,
				},
			],
		},
	});

	humidityChart = new Chart(document.getElementById("humidityChart"), {
		type: "line",
		data: {
			labels: labels,
			datasets: [
				{
					label: "Humidity (%)",
					data: humidity,
					borderColor: "blue",
					backgroundColor: "lightblue",
					tension: 0.3,
				},
			],
		},
	});

	windChart = new Chart(document.getElementById("windChart"), {
		type: "line",
		data: {
			labels: labels,
			datasets: [
				{
					label: "Wind Speed",
					data: wind,
					borderColor: "green",
					backgroundColor: "lightgreen",
					tension: 0.3,
				},
			],
		},
	});
}

setInterval(() => {
	if (currentCity) {
		fetchAndUpdate(currentCity);
	}
}, 30000);
