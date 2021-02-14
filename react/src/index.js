import React from 'react'
import ReactDOM from 'react-dom'
import Schedular from './components/Schedular'

let pull_id, user_id;

$(document).ready(function () {
  var query_url = window.location.href
  var url = new URL(query_url);

  pull_id = url.searchParams.get("id")
  pull_id = "b3yAVdroee";
  user_id = url.searchParams.get("name")
  user_id = "123";
})


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
      pull_id,
      user_id,
      dates: convertToFormat('YYYY/MM/DD hh:mm', schedule)
    }
    $.ajax({
      url: `http://127.0.0.1:8001/api/vote/save/date`,
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
        passScheduleOut = {postSchedule}
      />
    </React.StrictMode>,
    document.getElementById('schedular')
  )
