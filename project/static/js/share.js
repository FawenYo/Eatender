let pull_id;
let target;

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

    if (query_params.get("target") != null) {
        target = query_params.get("target")
        localStorage["target"] = target
    } else {
        if (query_url.searchParams.get("target") != null) {
            target = query_url.searchParams.get("target")
            localStorage["target"] = target
        } else {
            target = localStorage["target"]
        }
    }
    initializeLiff("1655422218-O3KRZNpK");
})

function initializeLiff(myLiffId) {
    liff
        .init({
            liffId: myLiffId,
        })
        .then(() => {
            initializeApp();
        })
        .catch(err => {
            console.log(err);
        });
}

function initializeApp() {
    // check if the user is logged in/out, and disable inappropriate button
    if (!liff.isLoggedIn()) {
        liff.login();
    } else {
        liff.getProfile()
            .then(profile => {
                $(".loading_page").fadeOut();
                document.getElementById("loading_page").setAttribute("style", "display: none;")
                $(".wrapper").fadeIn();
            })
            .catch(err => {
                console.log(err);
            });
    }
}


function sendShare() {
    if (!pull_id) {
        pull_id = localStorage["pull_id"]
        if (!pull_id) {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "查無投票池，請重新再試！",
                confirmButtonText: "確認",
            })
        }
    }
    const requestOptions = {
        method: 'GET',
        header: { 'Content-Type': 'application/json' },
        mode: 'same-origin'
    };
    const requestURL = `./api/liffshare?pull_id=${pull_id}&target=${target}`

    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                liff.shareTargetPicker(data.data)
                    .then(() => {
                        Swal.fire({
                            icon: "success",
                            title: "成功！",
                            text: "訊息已送出至聊天室囉～",
                            confirmButtonText: "確認",
                        }).then((result) => {
                            liff.closeWindow();
                        })
                    })
                    .catch((error) => {
                        console.log(error)
                        Swal.fire({
                            icon: "error",
                            title: "很抱歉！",
                            text: "發生錯誤！",
                            confirmButtonText: "確認",
                        })
                        const [majorVer, minorVer, patchVer] = (liff.getLineVersion() || "").split(".")

                        if (minorVer === undefined) {
                            console.log("ShareTargetPicker was canceled in external browser")
                            return
                        }

                        if (parseInt(majorVer) >= 10 && parseInt(minorVer) >= 10 && parseInt(patchVer) > 0) {
                            alert("ShareTargetPicker was canceled in LINE app")
                        }
                    })
            } else {
                Swal.fire({
                    icon: "error",
                    title: "很抱歉！",
                    text: data,
                    confirmButtonText: "確認",
                })
            }
        })
        .catch((error) => {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "發生錯誤，請重新再試！",
                confirmButtonText: "確認",
            })
            console.log(error)
        });
}
