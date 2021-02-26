import React from 'react'
import ReactDOM from 'react-dom'
import Schedular from './components/Schedular'

let pull_id, user_id;
let lastSelect = [];
let header = "React Schedule Selector";
let subHeader = "Tap to select one time or drag to select multiple times at once.";
let [startYear, startMonth, startDate, num_days, min_time, max_time] = [2021, 3, 8, 4, 4, 14];

$(document).ready(function () {
  var query_url = window.location.href
  var url = new URL(query_url);

  pull_id = url.searchParams.get("id")
  user_id = url.searchParams.get("name")

  fetchScheduleParams();
})

function getWidth() {
  return Math.max(
    document.body.scrollWidth,
    document.documentElement.scrollWidth,
    document.body.offsetWidth,
    document.documentElement.offsetWidth,
    document.documentElement.clientWidth
  );
}

function fetchScheduleParams() {
  const requestOptions = {
    method: 'GET',
    header: { 'Content-Type': 'application/json' },
    mode: 'cors'
  };
  const requestURL = `/api/vote/get/date?pull_id=${pull_id}&user_id=${user_id}`

  fetch(requestURL, requestOptions)
    .then(response => response.json())
    .then((data) => {
      if (data.status == "success") {
        let fetchedData = data.data;
        lastSelect = fetchedData.last_select;

        for (let i = 0; i < lastSelect.length; i++) {
          lastSelect[i] = new Date(lastSelect[i])
        }

        header = fetchedData.vote_name;
        subHeader = `投票截止日期：${fetchedData.vote_end}\n拖曳或點擊以選擇時間`;

        let dateString = fetchedData.start_date.split('/');
        startYear = dateString[0];
        startMonth = dateString[1];
        startDate = dateString[2];

        num_days = fetchedData.num_days;
        min_time = fetchedData.min_time;
        max_time = fetchedData.max_time;

        ReactDOM.render(
          <React.StrictMode>
            <Schedular
              header={header}
              subHeader={subHeader}
              startYear={startYear}
              startMonth={startMonth}
              startDate={startDate}
              num_days={num_days}
              min_time={min_time}
              max_time={max_time}
              passScheduleOut={postSchedule}
              lastSelect={lastSelect}
              hoveredColor="rgba(89, 154, 242, 1)"
            />
          </React.StrictMode>,
          document.getElementById('schedular')
        )

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
        text: "發生錯誤，請重新再試！",
        confirmButtonText: "確認",
      })
      console.log(error)
    });
}

function postSchedule(schedule) {
  let isSelectingSchedule = !document.querySelector("#schedular").classList.contains('hidden');
  if (isSelectingSchedule) {
    let sendData = {
      pull_id,
      user_id,
      dates: schedule
    }
    const requestOptions = {
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sendData),
      mode: 'cors'
    };
    const requestURL = "/api/vote/save/date"

    fetch(requestURL, requestOptions)
      .then(response => response.json())
      .then((data) => {
        if (data.status == "success") {
          Lobibox.notify(
            'success',
            {
              delay: 1000,
              icon: true,
              iconSource: "fontAwesome",
              showAfterPrevious: true,
              msg: "已成功儲存！",
              width: getWidth()
            }
          );
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
          text: "發生錯誤，請重新再試！",
          confirmButtonText: "確認",
        })
        console.log(error)
      });
  }
}

