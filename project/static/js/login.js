let pull_id;
$(document).ready(function () {
  const query_url = new URL(window.location.href)
  const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))

  pull_id = query_params.get("id")
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
