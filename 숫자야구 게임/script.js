// 게임에 필요한 변수 선언
let randomNumbers = []; // 정답 숫자 3개를 저장할 배열
let attempts = 9;       // 남은 시도 횟수
let gameEnded = false;  // 게임 종료 여부

// 페이지가 로드되면 게임 초기화
window.onload = () => {
  initGame();
};

// 게임을 처음부터 초기화하는 함수
function initGame() {
  randomNumbers = generateRandomNumbers(); // 중복 없는 랜덤 숫자 3개 생성
  attempts = 9;
  gameEnded = false;

  // 시도 횟수 초기화
  document.getElementById("attempts").textContent = attempts;

  // 결과 이미지 초기화
  document.getElementById("game-result-img").src = "";

  // 결과 기록 초기화
  document.getElementById("results").innerHTML = "";

  // 입력창 초기화 및 활성화
  const inputs = document.querySelectorAll(".input-field");
  inputs.forEach(input => {
    input.disabled = false;
    input.value = "";
  });

  // 확인 버튼 활성화
  document.querySelector(".submit-button").disabled = false;
}

// 중복되지 않는 0~9 사이의 숫자 3개 생성
function generateRandomNumbers() {
  const nums = new Set();
  while (nums.size < 3) {
    const rand = Math.floor(Math.random() * 10);
    nums.add(rand);
  }
  return [...nums];
}

// 숫자 비교 및 판정 함수
function check_numbers() {
  if (gameEnded) return; // 게임 종료 시 무시

  // input에서 숫자 3개 읽기
  const inputs = [
    document.getElementById("number1").value,
    document.getElementById("number2").value,
    document.getElementById("number3").value
  ];

  if (inputs.some(v => v === "")) {
    
    // input 비워주기
    document.getElementById("number1").value = "";
    document.getElementById("number2").value = "";
    document.getElementById("number3").value = "";

    return;
  }

  // 숫자형으로 변환 및 중복 검사
  const guess = inputs.map(Number);
  const uniqueGuess = new Set(guess);
if (uniqueGuess.size !== 3) {
  alert("중복되지 않는 숫자 3개를 입력하세요.");

  // 입력창 초기화 추가
  document.getElementById("number1").value = "";
  document.getElementById("number2").value = "";
  document.getElementById("number3").value = "";

  return;
}

  // 스트라이크/볼 계산
  let strike = 0, ball = 0;
  for (let i = 0; i < 3; i++) {
    if (guess[i] === randomNumbers[i]) {
      strike++;
    } else if (randomNumbers.includes(guess[i])) {
      ball++;
    }
  }

// 결과 UI 구성
const resultDiv = document.createElement("div");
resultDiv.className = "check-result";
resultDiv.style.display = "flex";
resultDiv.style.alignItems = "center";
resultDiv.style.margin = "8px 0";

// 왼쪽: 입력 숫자 표시
const left = document.createElement("div");
left.className = "left";
left.style.display = "flex";
left.style.gap = "8px";
guess.forEach(num => {
  const span = document.createElement("span");
  span.textContent = num;
  span.className = "num-result";
  left.appendChild(span);
});

// 가운데 콜론(:)
const center = document.createElement("div");
center.className = "center";
center.textContent = ":";
center.style.margin = "0 12px";
center.style.fontWeight = "bold";

// 오른쪽: 결과 출력
const right = document.createElement("div");
right.className = "right";
right.style.display = "flex";
right.style.gap = "12px";

// 결과 구성
if (strike === 0 && ball === 0) {
  const out = document.createElement("span");
  out.textContent = "O";
  out.className = "num-result out";
  right.appendChild(out);
} else {
  const sWrap = document.createElement("span");
  sWrap.style.display = "flex";
  sWrap.style.alignItems = "center";

  const sNum = document.createElement("span");
  sNum.textContent = strike;

  const sAlpha = document.createElement("span");
  sAlpha.textContent = "S";
  sAlpha.className = "num-result strike";
  sAlpha.style.marginLeft = "2px";

  sWrap.appendChild(sNum);
  sWrap.appendChild(sAlpha);
  right.appendChild(sWrap);

  const bWrap = document.createElement("span");
  bWrap.style.display = "flex";
  bWrap.style.alignItems = "center";

  const bNum = document.createElement("span");
  bNum.textContent = ball;

  const bAlpha = document.createElement("span");
  bAlpha.textContent = "B";
  bAlpha.className = "num-result ball";
  bAlpha.style.marginLeft = "2px";

  bWrap.appendChild(bNum);
  bWrap.appendChild(bAlpha);
  right.appendChild(bWrap);
}

// 조립
resultDiv.appendChild(left);
resultDiv.appendChild(center);
resultDiv.appendChild(right);
document.getElementById("results").appendChild(resultDiv);

  // 시도 횟수 감소
  attempts--;
  document.getElementById("attempts").textContent = attempts;

  // 게임 승패 조건 판정
  if (strike === 3) {
    endGame("success"); // 정답
  } else if (attempts === 0) {
    endGame("fail"); // 실패
  }
}

// 게임 종료 처리 함수
function endGame(result) {
  gameEnded = true;

  // 확인 버튼 비활성화
  document.querySelector(".submit-button").disabled = true;

  // 입력창 비활성화
  const inputs = document.querySelectorAll(".input-field");
  inputs.forEach(input => input.disabled = true);

  // 결과 이미지 출력
  const img = document.getElementById("game-result-img");
  img.src = result === "success" ? "./success.png" : "./fail.png";
}