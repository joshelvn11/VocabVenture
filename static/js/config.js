const DEVMODE = true;
let SERVER_URL;
const SCORE_INCREASE = 20;
const SCORE_DECREASE = -5;

if (DEVMODE) {
  SERVER_URL = "http://127.0.0.1:8000";
} else {
  SERVER_URL = "https://vocabventure.onrender.com";
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export { SERVER_URL, SCORE_INCREASE, SCORE_DECREASE, getCookie };
