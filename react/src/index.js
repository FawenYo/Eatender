import React from 'react'
import ReactDOM from 'react-dom'
import Schedular from './components/Schedular'

let pull_id, user_id;
let startDate, num_days, min_time, max_time;
$(document).ready(function () {
  var query_url = window.location.href
  var url = new URL(query_url);

  pull_id = url.searchParams.get("id")
  pull_id = "b3yAVdroee";
  user_id = url.searchParams.get("name")
  user_id = "123";

  [startDate, num_days, min_time, max_time] = fetchScheduleParams();
})

function fetchScheduleParams(){
  $.ajax({
    url: `http://127.0.0.1:8001/api/vote/date/${pull_id}`,
    contentType: "application/json",
    method: "get",
    dataType: "json",
    success: function (data) {
        if (data.status == "success") {
          // RETURN
          console.log("RETURN SCHEDULAR PARAMS")
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
        console.log("error")
    },
})
}
function convertToFormat(format, dateArray){
  if (format == "YYYY/MM/DD hh:mm"){
    return dateArray.map((date)=>{
      return `${date.getFullYear()}/${date.getMonth()+1}/${date.getDate()} ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`
    })
  }
}
function postSchedule (schedule) {
  if (schedule.length != 0){
    let sendData = {
      user_id,
      dates: convertToFormat('YYYY/MM/DD hh:mm', schedule)
    }
    $.ajax({
      url: `http://127.0.0.1:8001/api/save/date`,
      contentType: "application/json",
      method: "post",
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
      _startDate = {new Date()}
      _numDays = {5}
      _minTime = {8}
      _maxTime = {22}
      passScheduleOut = {postSchedule}
    />
  </React.StrictMode>,
  document.getElementById('schedular')
)

