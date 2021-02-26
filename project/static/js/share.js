let pull_id

$(document).ready(function () {
    $("#btnShare").click(function (event) {
        sendShare()
    })
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
                const query_url = new URL(window.location.href)
                if (query_url.searchParams.has("liff.state")) {
                    const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))
                    pull_id = query_params.get("pull_id")
                } else {
                    pull_id = query_url.searchParams.get("pull_id")
                }
            })
            .catch(err => {
                console.log(err);
            });
    }
}


function sendShare() {
    $.ajax({
        url: `./api/liffshare?pull_id=${pull_id}`,
        contentType: "application/json",
        method: "get",
        dataType: "json",
        success: function (data) {
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
                    type: "error",
                    title: "很抱歉！",
                    text: data,
                    confirmButtonText: "確認",
                })
            }
        },
        error: function (e) {
            alert("發生錯誤！")
            console.log(e)
        },
    })
}
