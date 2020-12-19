$(document).ready(function () {
  pull_id = $("#pull_id").val();
  if (pull_id == "") {
    pull_id = readCookie("pull_id");
    console.log(pull_id);
  }

  initializeLiff("1655422218-8n1PlOw1");
});

function initializeLiff(myLiffId) {
  liff
    .init({
      liffId: myLiffId,
    })
    .then(() => {
      initializeApp();
    })
    .catch((err) => {
      console.log(err);
    });
}

function initializeApp() {
  // check if the user is logged in/out, and disable inappropriate button
  if (!liff.isLoggedIn()) {
    liff.login();
  } else {
    liff
      .getProfile()
      .then((profile) => {
        userId = profile.userId;
        userStatus(userId);
      })
      .catch((err) => {
        console.log(err);
      });
  }
}

function userStatus(userId) {
  pull_id = $("#pull_id").val();
  location.replace(`../vote?id=${pull_id}&name=${userId}`);
}

function saveUserInfo(pullID) {
  expire_days = 10; // 過期日期(天)
  var d = new Date();
  d.setTime(d.getTime() + expire_days * 24 * 60 * 60 * 1000);
  document.cookie = `pull_id=${pullID}; expires=${d.toGMTString()}; path=/`;
}

// 讀取Cookie
function readCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
