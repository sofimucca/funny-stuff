//Selector
let euro = document.querySelector("#euro");
let cappelletti = document.querySelector("#cappelletti");
let form = document.querySelector("form");
let result = document.querySelector(".result");

//Listener
form.addEventListener("submit", converter);

//Functions
function converter(e) {
  e.preventDefault();
  result.innerHTML = "";

  if (isNaN(euro.value)) {
    return false;
  }

  cappelletti.value = Math.floor(euro.value / 6.9)*10;

  for (let i = 0; i < cappelletti.value; i++) {
    let image = document.createElement("img");
    image.src = "./cappelletto-logo.png";
    image.classList.add("cappelletto-img");
    console.log("cappelletto");
    result.appendChild(image);
  }
}
