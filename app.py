
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mưa Từ Vựng - Bảo Vệ Trái Đất",
    page_icon="🌌",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #050b20;
    color: white;
}
h1, p {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌌 MƯA TỪ VỰNG")
st.caption("🛸 Gõ từ tiếng Anh để bảo vệ Trái Đất!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #03091c;
    color: white;
    font-family: Arial, sans-serif;
}
#hud {
    display: flex;
    justify-content: space-around;
    padding: 10px;
    background: #101b43;
    font-weight: bold;
    font-size: 16px;
}
#space {
    height: 430px;
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(ellipse at 20% 30%, #153b7a, transparent 40%),
      radial-gradient(ellipse at 80% 20%, #492574, transparent 40%),
      linear-gradient(#071b49, #020719);
}
.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s infinite alternate;
}
@keyframes twinkle {
    from { opacity: .25; }
    to { opacity: 1; }
}
#planet {
    position: absolute;
    bottom: -115px;
    left: -10%;
    width: 120%;
    height: 180px;
    border-radius: 50% 50% 0 0;
    background: radial-gradient(ellipse at 50% 0%,
      #a7d9ff, #325ba9 25%, #15295b 70%);
    box-shadow: 0 -8px 35px #438dff;
}
.meteor {
    position: absolute;
    min-width: 105px;
    text-align: center;
    padding: 9px 10px;
    border-radius: 14px;
    background: linear-gradient(140deg,
      #ffb24c, #f16a48 40%, #5c3a91);
    border: 2px solid #ffe2a5;
    box-shadow: 0 0 18px #ff9b52;
    color: white;
    font-size: 17px;
    font-weight: bold;
    text-shadow: 1px 2px 3px #35133c;
}
.meaning {
    display: block;
    font-size: 12px;
    font-weight: normal;
    margin-top: 4px;
}
#panel {
    padding: 12px;
    background: #0b1434;
}
#entry {
    display: flex;
    gap: 8px;
}
input {
    flex: 1;
    min-width: 0;
    padding: 12px;
    font-size: 17px;
    border-radius: 10px;
    border: 2px solid #6989ff;
    background: #101d42;
    color: white;
}
button {
    padding: 10px 14px;
    border: 0;
    border-radius: 10px;
    background: #6553d9;
    color: white;
    font-weight: bold;
    cursor: pointer;
}
#message {
    min-height: 24px;
    margin-top: 8px;
    color: #b9d8ff;
}
#start {
    margin: 10px 0;
    width: 100%;
    background: #168eac;
    font-size: 16px;
}
</style>
</head>
<body>
<div id="hud">
  <span>⭐ Điểm: <b id="score">0</b></span>
  <span>❤️ Mạng: <b id="lives">5</b></span>
  <span>🚀 Cấp: <b id="level">1</b></span>
</div>

<div id="space">
  <div id="planet"></div>
</div>

<div id="panel">
  <div>⌨️ Gõ từ tiếng Anh trên thiên thạch rồi nhấn Enter.</div>
  <div id="entry">
    <input id="answer" placeholder="Type the English word..."
      autocomplete="off" disabled>
    <button id="submit" disabled>PHÁ HỦY</button>
  </div>
  <div id="message">Nhấn BẮT ĐẦU để chơi!</div>
  <button id="start">🚀 BẮT ĐẦU CHƠI</button>
</div>

<script>
const space = document.getElementById("space");
const input = document.getElementById("answer");
const startButton = document.getElementById("start");
const submitButton = document.getElementById("submit");

const vocabulary = [
  ["beautiful", "xinh đẹp"],
  ["journey", "chuyến hành trình"],
  ["protect", "bảo vệ"],
  ["universe", "vũ trụ"],
  ["adventure", "cuộc phiêu lưu"],
  ["courage", "lòng can đảm"],
  ["discover", "khám phá"],
  ["environment", "môi trường"],
  ["knowledge", "kiến thức"],
  ["wonderful", "tuyệt vời"],
  ["challenge", "thử thách"],
  ["galaxy", "thiên hà"],
  ["future", "tương lai"],
  ["imagine", "tưởng tượng"],
  ["success", "thành công"],
  ["planet", "hành tinh"],
  ["science", "khoa học"],
  ["careful", "cẩn thận"],
  ["friendship", "tình bạn"],
  ["powerful", "mạnh mẽ"]
];

let meteors = [];
let score = 0;
let lives = 5;
let level = 1;
let running = false;
let lastSpawn = 0;
let lastFrame = 0;
let animationId = null;
let messageTimer = null;

function stars() {
  space.querySelectorAll(".star").forEach(e => e.remove());
  for (let i = 0; i < 65; i++) {
    const s = document.createElement("div");
    s.className = "star";
    s.style.left = Math.random() * 100 + "%";
    s.style.top = Math.random() * 90 + "%";
    const size = 1 + Math.random() * 2;
    s.style.width = size + "px";
    s.style.height = size + "px";
    s.style.animationDelay = Math.random() * 2 + "s";
    space.appendChild(s);
  }
}
stars();

function say(text, color) {
  const msg = document.getElementById("message");
  msg.textContent = text;
  msg.style.color = color || "#b9d8ff";
}

function spawnMeteor() {
  const word = vocabulary[
    Math.floor(Math.random() * vocabulary.length)
  ];
  const el = document.createElement("div");
  el.className = "meteor";
  el.innerHTML = "☄️ " + word[0] +
    '<span class="meaning">' + word[1] + '</span>';
  space.appendChild(el);

  const maxX = Math.max(0, space.clientWidth - 125);
  const x = Math.random() * maxX;

  const meteor = {
    word: word[0],
    meaning: word[1],
    x: x,
    y: -65,
    speed: 24 + level * 9 + Math.random() * 12,
    el: el
  };

  el.style.left = x + "px";
  el.style.top = meteor.y + "px";
  meteors.push(meteor);
}

function updateHUD() {
  document.getElementById("score").textContent = score;
  document.getElementById("lives").textContent = lives;
  level = 1 + Math.floor(score / 50);
  document.getElementById("level").textContent = level;
}

function endGame() {
  running = false;
  cancelAnimationFrame(animationId);
  input.disabled = true;
  submitButton.disabled = true;
  startButton.textContent = "🔄 CHƠI LẠI";
  say("🌍 Kết thúc! Bạn đạt " + score +
    " điểm. Nhấn CHƠI LẠI để thử lần nữa.", "#ffcf86");
}

function loop(time) {
  if (!running) return;

  const dt = Math.min((time - (lastFrame || time)) / 1000, 0.05);
  lastFrame = time;

  const interval = Math.max(850, 1900 - level * 100);
  if (time - lastSpawn > interval) {
    spawnMeteor();
    lastSpawn = time;
  }

  for (let i = meteors.length - 1; i >= 0; i--) {
    const m = meteors[i];
    m.y += m.speed * dt;
    m.el.style.top = m.y + "px";

    if (m.y > space.clientHeight - 55) {
      m.el.remove();
      meteors.splice(i, 1);
      lives--;
      updateHUD();
      say("💫 Bỏ lỡ từ: " + m.word + " — " +
        m.meaning, "#ffaaaa");

      if (lives <= 0) {
        endGame();
        return;
      }
    }
  }

  animationId = requestAnimationFrame(loop);
}

function destroyWord() {
  if (!running) return;
  const typed = input.value.trim().toLowerCase();
  if (!typed) return;

  const index = meteors.findIndex(
    m => m.word.toLowerCase() === typed
  );

  if (index >= 0) {
    const m = meteors[index];
    m.el.remove();
    meteors.splice(index, 1);
    score += 10;
    updateHUD();
    say("✨ Chính xác! " + m.word +
      " = " + m.meaning + " (+10 điểm)", "#8dffbd");
    input.value = "";
  } else {
    say("Chưa thấy từ đó trên màn hình. Hãy kiểm tra lại nhé!",
      "#ffd38a");
  }
  input.focus();
}

input.addEventListener("keydown", e => {
  if (e.key === "Enter") {
    e.preventDefault();
    destroyWord();
  }
});
submitButton.addEventListener("click", destroyWord);

startButton.addEventListener("click", () => {
  cancelAnimationFrame(animationId);
  meteors.forEach(m => m.el.remove());
  meteors = [];
  score = 0;
  lives = 5;
  level = 1;
  lastSpawn = 0;
  lastFrame = 0;
  running = true;
  updateHUD();
  input.disabled = false;
  submitButton.disabled = false;
  startButton.textContent = "🔄 CHƠI LẠI";
  say("🚀 Bắt đầu! Gõ đúng từ trước khi chạm hành tinh.");
  input.value = "";
  input.focus();
  animationId = requestAnimationFrame(loop);
});
</script>
</body>
</html>
"""

components.html(game, height=590, scrolling=False)
