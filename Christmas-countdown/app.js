//Selector

let daysBox = document.querySelector(".days");
let hoursBox = document.querySelector(".hours");
let minutesBox = document.querySelector(".minutes");
let secondsBox = document.querySelector(".seconds");
let todos = document.querySelectorAll("li");
console.log(todos);

//Listeners

document.addEventListener("DOMContentLoaded", countDown);
todos.forEach(function (e) {
  console.log(e);
  e.addEventListener("click", completed);
});

//Functions

function countDown() {
  setInterval(function () {
    //Get year
    let today = new Date();
    let year = today.getFullYear();

    //Get time in milliseconds
    let christmas = new Date(year, 11, 25).getTime();
    let now = today.getTime();

    //Time in milliseconds
    let time = christmas - now;

    //Time in seconds
    let seconds = Math.floor(time / 1000);

    let days = Math.floor(seconds / (24 * 60 * 60));
    daysBox.innerText = days;

    seconds = seconds % (24 * 60 * 60);

    let hours = Math.floor(seconds / (60 * 60));
    hoursBox.innerText = hours;

    seconds = seconds % (60 * 60);

    let minutes = Math.floor(seconds / 60);
    minutesBox.innerText = minutes;

    seconds = seconds % 60;
    secondsBox.innerText = seconds;
  }, 1000);
}

function completed(e) {
  const item = e.target;
  item.classList.toggle("completed");
  console.log("click");
}
