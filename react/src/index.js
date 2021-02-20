import React from 'react'
import ReactDOM from 'react-dom'
import Schedular from './components/Schedular'

let pull_id, user_id;

$(document).ready(function () {
  var query_url = window.location.href
  var url = new URL(query_url);

  pull_id = url.searchParams.get("id")
  user_id = url.searchParams.get("name")
})


function postSchedule(schedule) {
  if (schedule.length != 0) {
    let sendData = {
      pull_id,
      user_id,
      dates: schedule
    }
    $.ajax({
      url: `http://0.0.0.0:8001/api/vote/save/date`,
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

ReactDOM.render(
  <React.StrictMode>
    <Schedular
      passScheduleOut={postSchedule}
    />
  </React.StrictMode>,
  document.getElementById('schedular')
)
