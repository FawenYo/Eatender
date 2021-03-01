let availableDate = {}

function okButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: green;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: light-gray;")

    availableDate[buttonDate] = "ok"
}

function unsureButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: orange;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: light-gray;")

    availableDate[buttonDate] = "unsure"
}

function cancelButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: red;");

    availableDate[buttonDate] = "cancel"
}

function submitButton() {
    let query_url = window.location.href
    let url = new URL(query_url);
    pull_id = url.searchParams.get("id")
    user_id = url.searchParams.get("name")

    let sendData = {
        pull_id,
        user_id,
        available_date: availableDate
    }
    const requestOptions = {
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sendData),
        mode: 'same-origin'
    };
    const requestURL = "/api/vote/save/date"
    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                Swal.fire({
                    icon: "success",
                    title: "投票成功！",
                    text: data.message,
                    confirmButtonText: "確認",
                })
            } else {
                Swal.fire({
                    icon: "error",
                    title: "很抱歉！",
                    text: data.error_message,
                    confirmButtonText: "確認",
                })
            }
        })
        .catch((error) => {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "發生錯誤，請重新再試！"
            })
            console.log(error)
        });
}