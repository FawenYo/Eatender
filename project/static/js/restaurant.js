var pull_id = ""
var user_id = ""
var total_restaurant = 0
var current_index = 0
var choose_result = { love: [], hate: [] }
var vote_link = ""

$(document).ready(function () {
    var query_url = window.location.href
    var url = new URL(query_url);

    pull_id = url.searchParams.get("id")
    user_id = url.searchParams.get("name")
    fetch_restaurant()
})

function fetch_restaurant() {
    $.ajax({
        url: `/api/vote/get/restaurant?pull_id=${pull_id}`,
        contentType: "application/json",
        method: "GET",
        dataType: "json",
        success: function (data) {
            if (data.status == "success") {
                restaurants = data.restaurants
                total_restaurant = restaurants.length
                restaurants.forEach(i => render(i))
                main()
            } else {
                Swal.fire({
                    type: "error",
                    title: "很抱歉！",
                    text: data.error_message,
                    confirmButtonText: "確認",
                })
            }
        },
        error: function () {
            Swal.fire({
                type: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
        },
    })
}

function render(i) {
    const data = `
    <div class="tinder--card">
            <div class="T1 fxLTR" dir="ltr">
               <div class="t1Header">
                  <div class="MdBx vr" id="7f6b6d4c-a7d1-4c00-ad27-3dc10640e659" style="padding:0px;">
                     <div class="MdBx hr" id="981434e3-d9af-4e42-9c68-82c1247c7e76">
                        <div class="ExCover MdImg ExFull" id="4a92bd98-dc4d-4623-9426-b78972cfd8b7">
                           <div><a style="padding-bottom:65%;"><span
                                    style="background-image:url('${i.photo_url}');"></span></a></div>
                        </div>
                     </div>
                  </div>
               </div>
               <div class="t1Body">
                  <div class="MdBx vr" id="a4f7f781-23b9-48c6-a019-161f3b4d2b90">
                     <div class="MdBx hr bl" id="0cb132a1-0dc2-4d6e-bd54-c0caaa38161a">
                        <div class="MdTxt ExFntStyNml ExXl fl0 ExWrap ExWB" id="b0e7f56f-2a7e-4953-856f-07a7ca1b9c50">
                           <p>${i.name}</p>
                        </div>
                     </div>
                     <div class="MdBx hr bl ExTMd" id="0b7e4af2-1e8e-471c-87ed-f33abd48476a">
                        <div class="MdTxt fl0 ExSm fxC0" id="b778ae34-fff4-4575-aeb2-17bdc82a0de1">
                           <p>評價: ${i.rating}</p>
                        </div>
                        <div class="fxC1 MdTxt ExMgnLMd fl0 ExSm" id="55474180-3979-4d02-bf60-f55bfe0e092f">
                           <p>平均價位: \$${i.price}</p>
                        </div>
                     </div>
                     <div class="MdBx hr bl ExTMd ExMgnTLg" id="03575cf1-e437-46de-bac1-30389a037ccf">
                        <div class="fxC2 MdTxt fl0 ExSm" id="2378b2fc-6c8e-40c9-91f6-0609a7af4abc">
                           <p>評論</p>
                        </div>
                        <div class="fxC2 MdTxt fl0 ExSm ExMgnLXl" id="1c520d53-4206-4f0f-bbc5-4d1f121e2196">
                           <p>${i.keywords[0]}</p>
                        </div>
                        <div class="fxC2 MdTxt ExMgnLMd fl0 ExSm" id="22108ab6-f36f-4999-ab14-dc4b2cdc42c0">
                           <p>${i.keywords[1]}</p>
                        </div>
                        <div class="fxC2 MdTxt ExMgnLMd fl0 ExSm" id="315ffc1c-813f-45a9-baf6-effab38d8773">
                           <p>${i.keywords[2]}</p>
                        </div>
                     </div>
                     <div class="spcSm MdBx vr ExMgnTLg" id="9a0dcf56-1454-46e1-9a21-a3b6d1f38f5c">
                        <div class="spcSm ExTLg MdBx hr bl ExBdrWdtBld" id="c270e5a6-2010-4629-b167-0755619690c1">
                           <div class="MdTxt fxC3 ExSm fl2" id="6c85a12a-6d49-4001-8773-921f263e52d6">
                              <p>地點</p>
                           </div>
                           <div class="MdTxt fxC3 ExSm ExWrap" id="ced78b13-d57e-467a-bc9d-5808597545d4"
                              style="-webkit-box-flex:6; flex-grow:6;">
                              <p>${i.address}</p>
                           </div>
                        </div>
                        <div class="spcSm MdBx ExBLg hr bl ExBdrWdtBld ExTSm" id="028fe3c0-74d7-4d8f-ab5a-463215095a15">
                           <div class="MdTxt fxC3 ExSm fl2" id="bbe15a22-7e7c-4dee-bc34-95cfc5588c80">
                              <p>電話</p>
                           </div>
                           <div class="MdTxt fxC3 ExSm ExWrap" id="83f9b9b6-3c9d-4011-9df4-9df44be5e250"
                              style="-webkit-box-flex:6; flex-grow:6;">
                              <p>${i.phone_number}</p>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>
         `
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
                vote_link = data.vote_link
                Swal.fire({
                    type: "success",
                    title: "儲存成功！",
                    text: "將在1秒後轉往日期投票...",
                    timer: 1000,
                })
            } else {
                Swal.fire({
                    type: "error",
                    title: "很抱歉！",
                    text: data.result,
                    confirmButtonText: "確認",
                })
            }
        },
        error: function () {
            Swal.fire({
                type: "error",
                title: "很抱歉！",
                text: "無法連接伺服器，請稍後再試！",
                confirmButtonText: "確認",
            })
        },
    })
}

function redirect() {
    location.replace(vote_link)
}
