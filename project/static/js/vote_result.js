let chartOption = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        xAxes: [{
            ticks: {
                beginAtZero: true
            }
        }],
    }
}
let best_label = [];
let best_data = [];
let restaurant_label = [];
let restaurant_data = [];
let date_label = [];
let date_data = [];
let most_best = [];
let most_restaurants = [];
let most_dates = [];
let filter_type = "best-filter";

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
        document.getElementById("bestChart").setAttribute("style", "display: block;")
        document.getElementById("restaurantChart").setAttribute("style", "display: none;")
        document.getElementById("dateChart").setAttribute("style", "display: none;")
        for (each in most_best) {
            data = `<li style="text-align: left;">${most_best[each]}</li>`
            $("#result-text").append(data)
        }
    } else if (filter == "restaurant-filter") {
        document.getElementById("bestChart").setAttribute("style", "display: none;")
        document.getElementById("restaurantChart").setAttribute("style", "display: block;")
        document.getElementById("dateChart").setAttribute("style", "display: none;")
        for (each in most_restaurants) {
            data = `<li style="text-align: left;">${most_restaurants[each]}</li>`
            $("#result-text").append(data)
        }
    } else {
        document.getElementById("bestChart").setAttribute("style", "display: none;")
        document.getElementById("restaurantChart").setAttribute("style", "display: none;")
        document.getElementById("dateChart").setAttribute("style", "display: block;")
        for (each in most_dates) {
            data = `<li style="text-align: left;">${most_dates[each]}</li>`
            $("#result-text").append(data)
        }
    }
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

                for (var i in data.data.best) {
                    best_label.push(i)
                    best_data.push(data.data.best[i])
                }
                for (var i in data.data.restaurants) {
                    restaurant_label.push(i)
                    restaurant_data.push(data.data.restaurants[i])
                }
                for (var i in data.data.dates) {
                    date_label.push(i)
                    date_data.push(data.data.dates[i])
                }
                renderChart()
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

function renderChart() {
    let best_ctx = document.getElementById('bestCanvas').getContext('2d');
    let restaurant_ctx = document.getElementById('restaurantCanvas').getContext('2d');
    let date_ctx = document.getElementById('dateCanvas').getContext('2d');
    let best_chart = new Chart(best_ctx, {
        // The type of chart we want to create
        type: 'horizontalBar',
        // The data for our dataset
        data: {
            labels: best_label,
            datasets: [{
                label: '投票可行人數',
                data: best_data,
                backgroundColor: palette('tol-rainbow', best_data.length).map((hex) => {
                    return '#' + hex;
                })
            }]
        },
        options: chartOption
    });
    let restaurant_chart = new Chart(restaurant_ctx, {
        // The type of chart we want to create
        type: 'horizontalBar',
        // The data for our dataset
        data: {
            labels: restaurant_label,
            datasets: [{
                label: '投票可行人數',
                data: restaurant_data,
                backgroundColor: palette('tol-rainbow', restaurant_data.length).map((hex) => {
                    return '#' + hex;
                })
            }]
        },
        options: chartOption
    });
    let date_chart = new Chart(date_ctx, {
        // The type of chart we want to create
        type: 'horizontalBar',
        // The data for our dataset
        data: {
            labels: date_label,
            datasets: [{
                label: '投票可行人數',
                data: date_data,
                backgroundColor: palette('tol-rainbow', date_data.length).map((hex) => {
                    return '#' + hex;
                })
            }]
        },
        options: chartOption
    });
}