var pull_id = "";
$(document).ready(function () {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  if (urlParams.has("liff.state")) {
    param = urlParams.get("liff.state");
    pull_id = param.substring(4);
  } else if (urlParams.has("id")) {
    pull_id = urlParams.get("id");
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
  location.replace(`../vote?id=${pull_id}&name=${userId}`);
}
