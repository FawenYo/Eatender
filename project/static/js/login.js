let pull_id;
$(document).ready(function () {
	const query_url = new URL(window.location.href)
	const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))

	if (query_params.get("pull_id") != null) {
		pull_id = query_params.get("pull_id")
		localStorage["pull_id"] = pull_id
	} else {
		if (query_url.searchParams.get("pull_id") != null) {
			pull_id = query_url.searchParams.get("pull_id")
			localStorage["pull_id"] = pull_id
		} else {
			pull_id = localStorage["pull_id"]
		}
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

function userStatus(userID) {
	location.replace(`../vote?id=${pull_id}&name=${userID}`);
}
