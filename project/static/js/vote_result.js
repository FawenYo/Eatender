let most_best = [];
let most_restaurants = [];
let most_dates = [];
let filter_type = "best-filter";
let vote_data;
let user_count = 0;

$(document).ready(() => {
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
    fetchData()

    // 篩選結果
    $("#type-category-tool .type").click(function () {
        if ($(this).hasClass("active") == false) {
            filter_type = $(this).data("type")
            $("#type-category-tool .type").removeClass("active")
            $(this).addClass("active")
            changeChart(filter_type)
        }
    })
})

function changeChart(filter) {
    $("#result-text").empty()
    $("#result-text").append(`<h4>最多人選擇：</h4>`)
    if (filter == "best-filter") {
        for (each in most_best) {
            data = `<li style="text-align: left;">${most_best[each]}</li>`
            $("#result-text").append(data)
        }
    } else if (filter == "restaurant-filter") {
        for (each in most_restaurants) {
            data = `<li style="text-align: left;">${most_restaurants[each]}</li>`
            $("#result-text").append(data)
        }
    } else {
        for (each in most_dates) {
            data = `<li style="text-align: left;">${most_dates[each]}</li>`
            $("#result-text").append(data)
        }
    }
    renderChart(filter_type)
}

function fetchData() {
    const requestOptions = {
        method: 'GET',
        header: { 'Content-Type': 'application/json' },
        mode: 'same-origin'
    };
    const requestURL = `/api/vote/get/result?pull_id=${pull_id}`

    fetch(requestURL, requestOptions)
        .then(response => response.json())
        .then((data) => {
            if (data.status == "success") {
                most_best = data.data.most_best
                most_restaurants = data.data.most_restaurants
                most_dates = data.data.most_dates

                document.getElementById("vote-title").innerHTML = data.data.vote_name;

                vote_data = data.data
                user_count = data.data.total_users
                renderChart(filter_type)
                changeChart(filter_type)
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

function renderChart(filter) {
    let detail = "";
    $("#Chart").empty()
    if (filter == "best-filter") {
        for (i in vote_data.best) {
            const voteInfo = i
            const infoCount = vote_data.best[i]
            const percent = infoCount / user_count
            const temp = `
                <div class="progressBar">
                    <h4>${voteInfo} (${infoCount}人)</h4>
                    <div class="progressBarContainer">
                        <div class="progressBarValue" style="width: ${percent * 100}%; background: #f5ba1b;"></div>
                    </div>
                </div>
            `
            detail += temp
        }
    } else if (filter == "restaurant-filter") {
        for (i in vote_data.restaurants) {
            const voteInfo = i
            const infoCount = vote_data.restaurants[i]
            const percent = infoCount / user_count
            const temp = `
                <div class="progressBar">
                    <h4>${voteInfo} (${infoCount}人)</h4>
                    <div class="progressBarContainer">
                        <div class="progressBarValue" style="width: ${percent * 100}%; background: #f5ba1b;"></div>
                    </div>
                </div>
            `
            detail += temp
        }
    } else {
        for (i in vote_data.dates) {
            const voteInfo = i
            const infoCount = vote_data.dates[i]
            const percent = infoCount / user_count
            const temp = `
                <div class="progressBar">
                    <h4>${voteInfo} (${infoCount}人)</h4>
                    <div class="progressBarContainer">
                        <div class="progressBarValue" style="width: ${percent * 100}%; background: #f5ba1b;"></div>
                    </div>
                </div>
            `
            detail += temp
        }
    }

    const data = `
            <div class="chart-container" id="chart-container">
                <div class="row">
                    <div class="eight columns">
                        ${detail}
                    </div>
                </div>
            </div>
        `
    $("#Chart").append(data)
}