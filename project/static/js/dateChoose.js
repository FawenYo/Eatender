let availableDate = {}

function okButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: green;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: light-gray;")

    document.getElementById(`ok_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_ok`]) + 1
    document.getElementById(`unsure_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_unsure`])
    document.getElementById(`cancel_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_cancel`])

    availableDate[buttonDate] = "ok"
}

function unsureButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: orange;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: light-gray;")

    document.getElementById(`ok_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_ok`])
    document.getElementById(`unsure_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_unsure`]) + 1
    document.getElementById(`cancel_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_cancel`])

    availableDate[buttonDate] = "unsure"
}

function cancelButton(targetBtn) {
    let clickedBtnID = targetBtn.attr('id');
    let buttonDate = clickedBtnID.split("_")[1];
    document.getElementById(`ok_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`unsure_${buttonDate}`).setAttribute("style", "color: light-gray;")
    document.getElementById(`cancel_${buttonDate}`).setAttribute("style", "color: red;");

    document.getElementById(`ok_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_ok`])
    document.getElementById(`unsure_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_unsure`])
    document.getElementById(`cancel_users_count_${buttonDate}`).innerText = parseInt(localStorage[`${buttonDate}_cancel`]) + 1

    availableDate[buttonDate] = "cancel"
}

function submitButton() {
    let validate = true
    pull_id = localStorage["pull_id"];
    user_id = localStorage["user_id"];
    let totalDates = localStorage["totalDates"].split(",");
    for (each in totalDates) {
        eachDate = totalDates[each]
        if (!availableDate[eachDate]) {
            validate = false
        }
    }
    if (validate) {
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
                        confirmButtonText: "離開投票",
                        showCancelButton: true,
                        cancelButtonText: "查看結果",
                    }).then((result) => {
                        if (result.isConfirmed) {
                            liff.closeWindow();
                        } else {
                            window.location.replace(`https://liff.line.me/1655422218-KOeZvV1e?pull_id=${pull_id}&target=result`);
                        }
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
    } else {
        Swal.fire({
            icon: "error",
            title: "很抱歉！",
            text: "尚有日期未選擇",
            confirmButtonText: "確認",
        })
    }
}