let tempChart = null
let humidityChart = null
let windChart = null

let currentCity = null

async function loadWeather(){

currentCity = document.getElementById("city").value

await fetchAndUpdate(currentCity)

}

async function fetchAndUpdate(city){

const response = await fetch(`http://127.0.0.1:8000/history/${city}`)
const data = await response.json()

console.log(data)

const temps = data.map(d => d.temperature)
const humidity = data.map(d => d.humidity)
const wind = data.map(d => d.wind_speed)

const labels = data.map(d =>
new Date(d.time).toLocaleTimeString()
)

if(tempChart){tempChart.destroy()}
if(humidityChart){humidityChart.destroy()}
if(windChart){windChart.destroy()}

tempChart = new Chart(
document.getElementById("tempChart"),
{
type:"line",
data:{
labels:labels,
datasets:[{
label:"Temperature (°C)",
data:temps,
borderColor:"red",
backgroundColor:"pink",
tension:0.3
}]
}
})

humidityChart = new Chart(
document.getElementById("humidityChart"),
{
type:"line",
data:{
labels:labels,
datasets:[{
label:"Humidity (%)",
data:humidity,
borderColor:"blue",
backgroundColor:"lightblue",
tension:0.3
}]
}
})

windChart = new Chart(
document.getElementById("windChart"),
{
type:"line",
data:{
labels:labels,
datasets:[{
label:"Wind Speed",
data:wind,
borderColor:"green",
backgroundColor:"lightgreen",
tension:0.3
}]
}
})

checkHeatwave(city)

}

setInterval(() => {

if(currentCity){
fetchAndUpdate(currentCity)
}

}, 30000)