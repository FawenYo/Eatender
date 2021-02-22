let pull_id

$(document).ready(function () {
    $("#btnShare").click(function (event) {
        sendShare()
    })
    const query_url = new URL(window.location.href)
    const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))

    pull_id = query_params.get("pull_id")

    main()
})

async function main() {
    await liff.init({ liffId: "1655422218-O3KRZNpK" })
    if (liff.isLoggedIn()) {
        document.getElementById("btnShare").style.display = "block"
    } else {
        liff.login()
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
            console.log(e)
        },
    })
}
