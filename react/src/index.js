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

function fetchScheduleParams() {
  $.ajax({
    url: "http://localhost:8001/api/vote/get/date",
    contentType: "application/json",
    method: "GET",
    data: {
      pull_id: pull_id,
      user_id: user_id
    },
    dataType: "json",
    success: function (data) {
      if (data.status == "success") {
        let fetchedData = data.data;
        lastSelect = fetchedData.last_select;

        for (let i = 0; i < lastSelect.length; i++) {
          lastSelect[i] = new Date(lastSelect[i])
        }

        console.log("lastSelect: ", lastSelect)
        
        header = fetchedData.vote_name;
        subHeader = `投票截止日期：${fetchedData.vote_end}`;

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
    },
    error: function () {
      console.log("error")
    },
  })
}

function postSchedule(schedule) {
  let isSelectingSchedule = !document.querySelector("#schedular").classList.contains('hidden');
  if (isSelectingSchedule) {
    let sendData = {
      pull_id,
      user_id,
      dates: schedule
    }
    $.ajax({
      url: `http://localhost:8001/api/vote/save/date`,
      contentType: "application/json",
      method: "POST",
      dataType: "json",
      data: JSON.stringify(sendData),
      success: function (data) {
        if (data.status == "success") {
          console.log('uploaded data: ', sendData)
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
        init()
      },
    })
  }
}

