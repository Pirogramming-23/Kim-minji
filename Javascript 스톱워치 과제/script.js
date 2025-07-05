let startTime;
let elapsedTime = 0;
let timerInterval;
let timerLimit = null; // 타이머 제한 시간 (ms)

const timeDisplay = document.getElementById("time");
const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const resetButton = document.getElementById("reset");
const lapRecords = document.getElementById("lap-records");
const deleteSelectedBtn = document.getElementById("delete-selected");
const selectAllCheckbox = document.getElementById("select-all");
const timerInput = document.getElementById("timer-input");

function formatTime(ms) {
  const totalCentiseconds = Math.floor(ms / 10);
  const seconds = String(Math.floor(totalCentiseconds / 100)).padStart(2, "0");
  const centiseconds = String(totalCentiseconds % 100).padStart(2, "0");
  return `${seconds}:${centiseconds}`;
}

function updateDisplay() {
  const now = Date.now();
  const diff = now - startTime + elapsedTime;
  timeDisplay.textContent = formatTime(diff);

  // 타이머 기능
  if (timerLimit !== null && diff >= timerLimit) {
    clearInterval(timerInterval);
    timerInterval = null;
    elapsedTime = timerLimit;
    timeDisplay.textContent = formatTime(timerLimit);
    alert("타이머 완료!");
  }
}

startButton.addEventListener("click", () => {
  if (timerInterval) return;

  const seconds = Number(timerInput.value);
  timerLimit = seconds > 0 ? seconds * 1000 : null;

  startTime = Date.now();
  timerInterval = setInterval(updateDisplay, 10);
});

stopButton.addEventListener("click", () => {
  if (!timerInterval) return;
  clearInterval(timerInterval);
  timerInterval = null;
  elapsedTime += Date.now() - startTime;

  // 기록 추가
  const lap = document.createElement("div");
  lap.classList.add("lap-record");

  const label = document.createElement("label");
  label.classList.add("circle-checkbox");

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";

  // 개별 체크 시 전체 선택 해제 여부 판단
  checkbox.addEventListener("change", () => {
    const all = document.querySelectorAll(".lap-record input[type='checkbox']");
    const allChecked = [...all].every(cb => cb.checked);
    selectAllCheckbox.checked = allChecked;
  });

  if (selectAllCheckbox.checked) checkbox.checked = true;

  const circle = document.createElement("span");
  circle.classList.add("circle-mark");

  label.appendChild(checkbox);
  label.appendChild(circle);

  const timeSpan = document.createElement("span");
  timeSpan.classList.add("lap-time");
  timeSpan.textContent = formatTime(elapsedTime);

  lap.appendChild(label);
  lap.appendChild(timeSpan);
  lapRecords.appendChild(lap);
});

resetButton.addEventListener("click", () => {
  clearInterval(timerInterval);
  timerInterval = null;
  elapsedTime = 0;
  timerLimit = null;
  timeDisplay.textContent = "00:00";
  // 기록은 유지
});

deleteSelectedBtn.addEventListener("click", () => {
  const all = document.querySelectorAll(".lap-record");
  all.forEach((lap) => {
    const checkbox = lap.querySelector("input[type='checkbox']");
    if (checkbox.checked) lap.remove();
  });
});

selectAllCheckbox.addEventListener("change", () => {
  const all = document.querySelectorAll(".lap-record input[type='checkbox']");
  all.forEach(cb => cb.checked = selectAllCheckbox.checked);
});