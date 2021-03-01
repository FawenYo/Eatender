let pull_id

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
                console.log("LINE logged in!")
            })
            .catch(err => {
                console.log(err);
            });
    }
}


function sendShare() {
    const requestOptions = {
        method: 'GET',
        header: { 'Content-Type': 'application/json' },
        mode: 'same-origin'
    };
    const requestURL = `./api/liffshare?pull_id=${pull_id}`

    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                const result = liff.shareTargetPicker([
                    {
                        type: "flex",
                        altText: "一起來吃飯吧！",
                        contents: data.data,
                    },
                ])
                if (result) {
                    console.log(`[${result.status}] Message sent!`)
                } else {
                    const [majorVer, minorVer, patchVer] = (liff.getLineVersion() || "").split(".")

                    if (minorVer === undefined) {
                        console.log("ShareTargetPicker was canceled in external browser")
                        return
                    }

                    if (parseInt(majorVer) >= 10 && parseInt(minorVer) >= 10 && parseInt(patchVer) > 0) {
                        alert("ShareTargetPicker was canceled in LINE app")
                    }
                }
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
