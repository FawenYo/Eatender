var pull_id = ""
var user_id = ""
var total_restaurant = 0
var current_index = 0
var choose_result = { love: [], hate: [] }
var load_done = false

$(document).ready(function () {
    var query_url = window.location.href
    var url = new URL(query_url);

    pull_id = url.searchParams.get("id")
    user_id = url.searchParams.get("name")
    var tinderContainer = document.querySelector(".tinder")
    var allCards = document.querySelectorAll(".tinder--card")

    function initCards(card, index) {
        var newCards = document.querySelectorAll(".tinder--card:not(.removed)")

        newCards.forEach(function (card, index) {
            card.style.zIndex = allCards.length - index
            card.style.transform = "scale(" + (20 - index) / 20 + ") translateY(-" + 30 * index + "px)"
            card.style.opacity = (10 - index) / 10
        })

        tinderContainer.classList.add("loaded")
    }

    initCards()
    fetch_restaurant()
})

function fetch_restaurant() {
    $.ajax({
        url: "/api/vote/get/restaurant",
        contentType: "application/json",
        method: "GET",
        data: {
            pull_id: pull_id
        },
        dataType: "json",
        success: function (data) {
            if (data.status == "success") {
                $("#cardWrapper").empty()
                restaurants = data.restaurants
                total_restaurant = restaurants.length
                restaurants.forEach(i => render(i))
                load_done = true
                main()
            } else {
                Swal.fire({
                    icon: "error",
                    title: "很抱歉！",
                    text: data.error_message,
                    confirmButtonText: "確認",
                })
            }
        },
        error: function () {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
        },
    })
}

function render(i) {
    const data = `<div class='tinder--card'>
    <div class='main-window' id='main-window'>
  
        <div class='restaurant-image' style="background-image: url('${i.photo_url}');">
          <div class='restaurant-name'>${i.name}</div>
        </div>
        <div class='restaurant-info'>
          <div class='address'>地點：${i.address}</div>
        </div>
  
        <div class='detail-info'>
          <div class='detail-info-elm'>評價<br><span class='lg'>${i.rating}</span></div>
          <div class='detail-info-elm'>價位<br><span class='lg'>\$${i.price}</span></div>
          <div class='detail-info-elm'>關鍵字<br><span class='sm'>${i.keywords.join(", ")}</span></div>
        </div>
  
      </div>
  
  </div>`
    $("#cardWrapper").append(data)
}

function main() {
    var tinderContainer = document.querySelector(".tinder")
    var allCards = document.querySelectorAll(".tinder--card")
    var nope = document.getElementById("nope")
    var love = document.getElementById("love")

    function initCards(card, index) {
        var newCards = document.querySelectorAll(".tinder--card:not(.removed)")

        newCards.forEach(function (card, index) {
            card.style.zIndex = allCards.length - index
            card.style.transform = "scale(" + (20 - index) / 20 + ") translateY(-" + 30 * index + "px)"
            card.style.opacity = (10 - index) / 10
        })

        tinderContainer.classList.add("loaded")
    }

    initCards()

    allCards.forEach(function (el) {
        var hammertime = new Hammer(el)

        hammertime.on("pan", function (event) {
            el.classList.add("moving")
        })

        hammertime.on("pan", function (event) {
            if (event.deltaX === 0) return
            if (event.center.x === 0 && event.center.y === 0) return

            tinderContainer.classList.toggle("tinder_love", event.deltaX > 0)
            tinderContainer.classList.toggle("tinder_nope", event.deltaX < 0)
            var xMulti = event.deltaX * 0.03
            var yMulti = event.deltaY / 80
            var rotate = xMulti * yMulti
            var cards = document.querySelectorAll(".tinder--card:not(.removed)")
            var card = cards[0]

            card.style.transform = "translate(" + event.deltaX + "px, " + event.deltaY + "px) rotate(" + rotate + "deg)"
        })

        hammertime.on("panend", function (event) {
            el.classList.remove("moving")
            tinderContainer.classList.remove("tinder_love")
            tinderContainer.classList.remove("tinder_nope")

            var moveOutWidth = document.body.clientWidth
            var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5
            var cards = document.querySelectorAll(".tinder--card:not(.removed)")
            var card = cards[0]

            card.classList.toggle("removed", !keep)

            if (keep) {
                card.style.transform = ""
            } else {
                if (event.deltaX > 0) {
                    love_restaurant()
                } else {
                    not_love_restaurant()
                }
                var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth)
                var toX = event.deltaX > 0 ? endX : -endX
                var endY = Math.abs(event.velocityY) * moveOutWidth
                var toY = event.deltaY > 0 ? endY : -endY
                var xMulti = event.deltaX * 0.03
                var yMulti = event.deltaY / 80
                var rotate = xMulti * yMulti

                card.style.transform =
                    "translate(" + toX + "px, " + (toY + event.deltaY) + "px) rotate(" + rotate + "deg)"
                initCards()
            }
        })
    })

    function createButtonListener(love) {
        return function (event) {
            var cards = document.querySelectorAll(".tinder--card:not(.removed)")
            var moveOutWidth = document.body.clientWidth * 1.5

            if (!cards.length) return false

            var card = cards[0]

            card.classList.add("removed")

            if (love) {
                love_restaurant()
                card.style.transform = "translate(" + moveOutWidth + "px, -100px) rotate(-30deg)"
            } else {
                not_love_restaurant()
                card.style.transform = "translate(-" + moveOutWidth + "px, -100px) rotate(30deg)"
            }

            initCards()

            event.preventDefault()
        }
    }

    var nopeListener = createButtonListener(false)
    var loveListener = createButtonListener(true)

    nope.addEventListener("click", nopeListener)
    love.addEventListener("click", loveListener)
}

function love_restaurant() {
    choose_result["love"].push(current_index)
    current_index += 1
    if (current_index == total_restaurant) {
        save_results()
    }
}

function not_love_restaurant() {
    choose_result["hate"].push(current_index)
    current_index += 1
    if (current_index == total_restaurant) {
        save_results()
    }
}

function save_results() {
    // 請求資料
    const sendData = {
        pull_id: pull_id,
        user_id: user_id,
        choose_result: choose_result,
    }

    // 請求伺服器
    $.ajax({
        url: "/api/vote/save/restaurant",
        contentType: "application/json",
        method: "POST",
        dataType: "json",
        data: JSON.stringify(sendData),
        success: function (data) {
            if (data.status == "success") {
                Swal.fire({
                    icon: "success",
                    title: "儲存成功！",
                    text: "將在1秒後轉往日期投票...",
                    timer: 1000,
                })
                setTimeout(() => {
                    document.querySelector('#schedular').classList.remove('hidden')
                    document.querySelector('.tinder').classList.add('hidden')
                }, 1700)
            } else {
                Swal.fire({
                    icon: "error",
                    title: "很抱歉！",
                    text: data.result,
                    confirmButtonText: "確認",
                })
            }
        },
        error: function () {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
        },
    })
}
