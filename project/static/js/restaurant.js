let pull_id;
let user_id;
let total_restaurant = 0;
let current_index = 0;
let choose_result = { love: [], hate: [] };
let load_done = false;

$(document).ready(function () {
    if (!localStorage["dont_hint"] || localStorage["dont_hint"] == "false") {
        document.getElementById("hint_box").setAttribute("style", "display: block;");
        rightSlideIn(leftSlideIn);
    }

    //initializeLiff("1655422218-8n1PlOw1");
    parseParam();

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

function rightSlideIn(callback) {
    document.getElementById("left_content").setAttribute("style", "display: block; animation: right_slidein 1s;");
    setTimeout(callback, 1000);
}

function leftSlideIn() {
    document.getElementById("right_content").setAttribute("style", "display: block; animation: left_slidein 1s;");
}

function hideHint() {
    Swal.fire({
        icon: "question",
        title: "是否要永久關閉提示？",
        confirmButtonText: "確認",
        showCancelButton: true,
        cancelButtonText: "取消",
    }).then((result) => {
        if (result.isConfirmed) {
            localStorage["dont_hint"] = true
        }
    })
    document.getElementById("hint_box").setAttribute("style", "display: none;");
}

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
                user_id = profile.userId;
                localStorage["user_id"] = user_id
            })
            .catch((err) => {
                console.log(err);
            });
    }
}

function parseParam() {
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
}

function fetch_restaurant() {
    const requestOptions = {
        method: 'GET',
        header: { 'Content-Type': 'application/json' },
        mode: 'same-origin'
    };
    const requestURL = `/api/vote/get/restaurant?pull_id=${pull_id}`

    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                $("#cardWrapper").empty()
                restaurants = data.restaurants
                total_restaurant = restaurants.length
                restaurants.forEach(i => renderCard(i))
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
        })
        .catch((error) => {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
            console.log(error)
        });
}

function renderCard(restaurantInfo) {
    const data = `<div class='tinder--card'>
    <div class='main-window' id='main-window'>
  
        <div class='restaurant-image' style="background-image: url('${restaurantInfo.photo_url}');">
          <div class='restaurant-name'>${restaurantInfo.name}</div>
        </div>
        <div class='restaurant-info'>
          <div class='address'>地點：${restaurantInfo.address}</div>
        </div>
  
        <div class='detail-info'>
          <div class='detail-info-elm'>評價<br><span class='lg'>${restaurantInfo.rating}</span></div>
          <div class='detail-info-elm'>價位<br><span class='lg'>\$${restaurantInfo.price}</span></div>
          <div class='detail-info-elm'>關鍵字<br><span class='sm'>${restaurantInfo.keywords.join(", ")}</span></div>
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
    const sendData = {
        pull_id,
        user_id,
        choose_result,
    }
    const requestOptions = {
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sendData),
        mode: 'same-origin'
    };
    const requestURL = "/api/vote/save/restaurant"
    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                fetchVoteDate();
            } else {
                Swal.fire({
                    icon: "error",
                    title: "很抱歉！",
                    text: data.result,
                    confirmButtonText: "確認",
                })
            }
        })
        .catch((error) => {
            Swal.fire({
                icon: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
            console.log(error)
        });
}

function fetchVoteDate() {
    const requestOptions = {
        method: 'GET',
        header: { 'Content-Type': 'application/json' },
        mode: 'same-origin'
    };
    const requestURL = `/api/vote/get/date?pull_id=${pull_id}`

    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                Swal.fire({
                    icon: "success",
                    title: "儲存成功！",
                    text: "將在1秒後轉往日期投票...",
                    timer: 1000,
                });
                setTimeout(() => {
                    document.getElementsByTagName('body')[0].style = 'overflow: visible;';
                    document.querySelector('#schedular').classList.remove('hidden')
                    document.querySelector('.tinder').classList.add('hidden')
                }, 1700)
                document.getElementById("voteTitle").innerHTML = data.data.vote_name;
                $("#dateTable").empty()
                const voteTitle = `<h3>選擇時間</h3>`
                $("#dateTable").append(data)
                data.data.dates.forEach(i => renderDates(i))
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
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
            console.log(error)
        });
}

function renderDates(dateTitle) {
    const data = `<div class="date-info">
    <div class="date-title">
       <span>${dateTitle}</span>
    </div>
    <div class="date-choose">
       <button class="btn ok-icon" onclick="okButton($(this))" id="ok_${dateTitle}">
          <i class="fas fa-check-circle"></i>
       </button>
       <button class="btn unsure-icon" onclick="unsureButton($(this))" id="unsure_${dateTitle}">
          <i class="fas fa-question-circle"></i>
       </button>
       <button class="btn cancel-icon" onclick="cancelButton($(this))" id="cancel_${dateTitle}">
          <i class="fas fa-ban"></i>
       </button>
    </div>
 </div>`
    $("#dateTable").append(data)
}