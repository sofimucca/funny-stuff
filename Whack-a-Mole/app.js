function startGame() {
  sessionStorage.clear();
  timer(60);
  points();
  changeBtn();
  repeat();
}

function showMole() {
  erray = [];
  for (let i = 0; i < 6; i++) {
    erray[i] = i;
  }
  let bomb = isBomb(1, 3);
  let n = randomChoice(erray);
  let bush = document.getElementsByClassName("bush");
  if (bush[n]) {
    let classNmae;
    if (bomb) {
      bush[n].getElementsByClassName("bomb")[0].style.display = "block";
      className = "bomb";
    } else {
      bush[n].getElementsByClassName("mole")[0].style.display = "block";
      className = "mole";
    }
    setTimeout(() => {
      remove(bush[n], className);
    }, 1000);
    return true;
  } else {
    return false;
  }
}

function randomChoice(erray) {
  var i = Math.floor(Math.random() * erray.length);
  n = erray[i];
  erray.splice(i, 1);
  return n;
}

function isBomb(nTrue, nFalse) {
  let erray = [];
  for (let i = 0; i < nTrue; i++) {
    erray.push(true);
  }
  for (let i = 0; i < nFalse; i++) {
    erray.push(false);
  }
  return randomChoice(erray);
}

function remove(elm, className) {
  if (elm) {
    let child = elm.getElementsByClassName(className)[0];
    child.style.display = "none";
  }
}
function error(bomb) {
  bomb.src = "img/boom.png";
  setTimeout(() => {
    bomb.style.display = "none";
    bomb.src = "img/bomb.png";
  }, 500);
  points(false);
}

function removeMoleByClick(mole) {
  mole.style.display = "none";
  points(true);
}

function repeat() {
  let time = 1000 + Math.random() * 1000;
  let myTime = setTimeout(function () {
    if (showMole()) {
      repeat();
    }
  }, time);
}

function timer(n) {
  if (n == 0) {
    finishGame();
  } else {
    let timerSpan = document.getElementById("timer");
    if (timerSpan) {
      timerSpan.innerHTML = n;
      setTimeout(() => {
        timer(n - 1);
      }, 1000);
    }
  }
}

function points(x) {
  let n = sessionStorage.getItem("points");
  if (!n) {
    n = 0;
    sessionStorage.setItem("points", n);
  } else {
    if (x == true) {
      n = parseInt(n) + 50;
    } else {
      n = parseInt(n) - 200;
      if (n < 0) {
        n = 0;
      }
    }
    sessionStorage.setItem("points", n);
  }
  document.getElementById("points").innerHTML = n;
}
function changeBtn() {
  let btn = document.getElementById("btn");
  btn.innerHTML = "Finish";
  btn.onclick = function () {
    finishGame();
  };
}
function finishGame() {
  let n = sessionStorage.getItem("points");
  output = `<h1>Time's Up!!</h1>
  <div>Well done!You have made ${n} points.</div>
  <a href='index.html'>Click here to play again </a> `;
  document.getElementsByTagName("body")[0].innerHTML = output;
}
