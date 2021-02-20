window.onload = popup_show;

function popup_show() {
    Swal.fire({
        "icon": "success",
        "title": "綁定成功！",
        "text": "已經成功綁定LINE Notify，現在開始可以使用投票功能囉！",
        "confirmButtonText": "前往LINE Bot"
    }).then(() => {
        window.location.replace("https://lin.ee/0nShEox");
    })
}
