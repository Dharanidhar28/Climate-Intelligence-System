let tempChart = null;
let humidityChart = null;
let windChart = null;
let currentCity = null;

const searchedCities = [];

function setStatus(message, type = "neutral") {
	const badge = document.getElementById("statusBadge");
	badge.textContent = message;
	badge.className = `status-badge ${type}`;
}

function formatTime(value) {
	if (!value) {
		return "--";
	}

	return new Date(value).toLocaleTimeString([], {
		hour: "2-digit",
		minute: "2-digit",
	});
}

function renderSearchedCities() {
	const container = document.getElementById("searchedCities");

	if (!searchedCities.length) {
		container.innerHTML = '<span class="empty-chip">No cities searched yet</span>';
		return;
	}

	container.innerHTML = searchedCities
		.map((city) => `<button class="city-chip" data-city="${city}">${city}</button>`)
		.join("");

	document.querySelectorAll(".city-chip").forEach((button) => {
		button.addEventListener("click", async () => {
			const city = button.dataset.city;
			document.getElementById("city").value = city;
			await loadWeather(city);
		});
	});
}

function rememberCity(city) {
	const normalized = city.trim();
	const existingIndex = searchedCities.findIndex(
		(item) => item.toLowerCase() === normalized.toLowerCase()
	);

	if (existingIndex >= 0) {
		searchedCities.splice(existingIndex, 1);
	}

	searchedCities.unshift(normalized);
	renderSearchedCities();
}

function updateSummary(data) {
	document.getElementById("cityName").textContent = data.city;
	document.getElementById("conditionBadge").textContent = data.current_weather.condition;
	document.getElementById("conditionText").textContent = `Current condition: ${data.current_weather.description}`;
	document.getElementById("windowLabel").textContent = data.time_window.label;
	document.getElementById("windowStart").textContent = formatTime(data.time_window.start_local);
	document.getElementById("windowEnd").textContent = formatTime(data.time_window.end_local);

	document.getElementById("currentTemp").textContent = `${data.current_weather.temperature.toFixed(1)}°C`;
	document.getElementById("currentHumidity").textContent = `${data.current_weather.humidity.toFixed(0)}%`;
	document.getElementById("currentWind").textContent = `${data.current_weather.wind_speed.toFixed(1)} m/s`;
	document.getElementById("feelsLike").textContent = `${data.current_weather.feels_like.toFixed(1)}°C`;
	document.getElementById("pressure").textContent = `${data.current_weather.pressure} hPa`;
	document.getElementById("recordCount").textContent = data.summary.records_count;

	document.getElementById("avgTemp").textContent = `${data.summary.avg_temperature.toFixed(1)}°C`;
	document.getElementById("maxTemp").textContent = `${data.summary.max_temperature.toFixed(1)}°C`;
	document.getElementById("minTemp").textContent = `${data.summary.min_temperature.toFixed(1)}°C`;
	document.getElementById("tempTrend").textContent = data.summary.temperature_trend;
	document.getElementById("analysisText").textContent = data.analysis;

	const alertBox = document.getElementById("heatwaveAlert");
	if (data.heatwave) {
		alertBox.textContent = "Heatwave risk";
		alertBox.className = "alert-pill alert";
	} else {
		alertBox.textContent = "No heatwave";
		alertBox.className = "alert-pill safe";
	}

	const safetyList = document.getElementById("safetyList");
	safetyList.innerHTML = data.safety_measures.map((item) => `<li>${item}</li>`).join("");
}

function getChartConfig(label, labels, values, lineColor, fillColor) {
	return {
		type: "line",
		data: {
			labels,
			datasets: [
				{
					label,
					data: values,
					borderColor: lineColor,
					backgroundColor: fillColor,
					fill: true,
					tension: 0.35,
					pointRadius: 3,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: {
					display: false,
				},
			},
		},
	};
}

function updateCharts(history) {
	const labels = history.map((item) => formatTime(item.local_time || item.time));
	const temps = history.map((item) => item.temperature);
	const humidity = history.map((item) => item.humidity);
	const wind = history.map((item) => item.wind_speed);

	if (tempChart) {
		tempChart.destroy();
	}
	if (humidityChart) {
		humidityChart.destroy();
	}
	if (windChart) {
		windChart.destroy();
	}

	tempChart = new Chart(
		document.getElementById("tempChart"),
		getChartConfig("Temperature (°C)", labels, temps, "#ff7c4d", "rgba(255, 124, 77, 0.18)")
	);

	humidityChart = new Chart(
		document.getElementById("humidityChart"),
		getChartConfig("Humidity (%)", labels, humidity, "#3091ff", "rgba(48, 145, 255, 0.18)")
	);

	windChart = new Chart(
		document.getElementById("windChart"),
		getChartConfig("Wind Speed (m/s)", labels, wind, "#00a287", "rgba(0, 162, 135, 0.18)")
	);
}

async function loadWeather(selectedCity = null) {
	const city = selectedCity || document.getElementById("city").value.trim();

	if (!city) {
		setStatus("Enter a city name first.", "error");
		return;
	}

	try {
		setStatus("Loading weather timeline...", "neutral");

		const response = await fetch(`${API_BASE_URL}/history/${encodeURIComponent(city)}`);
		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.detail || data.message || "Unable to load weather data.");
		}

		currentCity = data.city;
		document.getElementById("city").value = data.city;
		rememberCity(data.city);
		updateSummary(data);
		updateCharts(data.history);
		setStatus(`Showing ${data.city} weather from 5 AM to now`, "success");
	} catch (error) {
		console.error(error);
		setStatus("Unable to load weather data.", "error");
		document.getElementById("analysisText").textContent = error.message;
	}
}

setInterval(() => {
	if (currentCity) {
		loadWeather(currentCity);
	}
}, 30000);

renderSearchedCities();
