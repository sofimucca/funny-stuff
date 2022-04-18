//Selectors
let container = document.querySelector(".container");
let dayBox = document.querySelector(".day");
let hoursBox = document.querySelector(".hours");
let minutesBox = document.querySelector(".minutes");
let secondsBox = document.querySelector(".seconds");
let imageBox = document.querySelector(".image-box");

//Events
imageBox.addEventListener("DOMContentLoaded", addImage());

//Functions
setInterval(function () {
  let now = new Date();
  let hours = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();
  let day = new Intl.DateTimeFormat("it-IT", { weekday: "short" }).format(now);

  hoursBox.innerText = hours;
  minutesBox.innerText = minutes;
  secondsBox.innerText = seconds;
  dayBox.innerText = day.toUpperCase();
}, 1000);

function addImage() {
  imageBox.innerHTML = "";
  let image = document.createElement("img");
  image.addEventListener("click", addImage);

  console.log("click");
  const api = "https://api.thecatapi.com/v1/images/search?size=full";

  fetch(api, {
    headers: {
      "x-api-key": "1b7c7ca7-e6f1-49cf-82b0-05b92681e91",
    },
    mode: "cors",
  })
    .then((response) => response.json())
    .then((result) => {
      console.log("Success:", result);
      let url = result[0].url;
      image.src = url;
    })
    .catch((error) => {
      console.error("Error:", error);
      let url = "./white-cat.jpg";
      image.src = url;
    });

  imageBox.appendChild(image);
}
