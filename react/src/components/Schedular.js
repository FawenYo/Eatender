import ScheduleSelector from 'react-schedule-selector';
import styled from 'styled-components';
import React, {useState} from 'react';


// 在要使用 schedular 的 js 檔中直接插入元件，並加入一個取得 schedule 的 callback。舉例如下： 
// 
//  <Schedular
//    passScheduleOut = {getSchedule}
//  ></Schedular>
// 
// passScheduleOut 會在使用者每次更改選擇時間後呼叫。
// 其需要在使用到 Schedular 的 js 檔中自行定義。
//
// 簡單的 passScheduleOut 範例：
// 
//  function passScheduleOut(schedule){ 
//    console.log(schedule); 
//  }
//
const Wrapper = styled.div`
  text-align: center;
  margin: 0 auto;
  width: 80%`;

const ScheduleWrapper = styled.div`
  padding: 20px;
  border-radius: 20px;
  background: white;
  box-shadow: 3px 5px 18px 0px rgba(191,191,191,0.76)`;

const H1 = styled.h1`
  font-size: 32pt`;

let pull_id;
let header = "React Schedule Selector";
let subHeader = "Tap to select one time or drag to select multiple times at once.";
let [startYear, startMonth, startDate, num_days, min_time, max_time] = [2021, 3, 8, 4, 4, 14];

window.onload = ()=>{
  let query_url = window.location.href
  let url = new URL(query_url);
  pull_id = url.searchParams.get("id");
  fetchScheduleParams();
}

function fetchScheduleParams(){
  $.ajax({
    url: `http://127.0.0.1:8001/api/vote/get/date?pull_id=${pull_id}`,
    contentType: "application/json",
    method: "get",
    dataType: "json",
    success: function (data) {
        if (data.status == "success") {
          // RETURN
          console.log("RETURN SCHEDULAR PARAMS")
          let fetchedData = data.data;
          let dateString = fetchedData.start_date.split('/');

          header = fetchedData.vote_name;
          subHeader = fetchedData.vote_end;
          startYear = dateString[0];
          startMonth = dateString[1];
          startDate = dateString[2];
          num_days = fetchedData.num_days;
          min_time = fetchedData.min_time;
          max_time = fetchedData.max_time;

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
        console.log("error dd")
    },
})
}

function Schedular({passScheduleOut}) {
  const [schedule, setSchedule] = useState([]);

  function handleChange(newSchedule) {
    setSchedule(newSchedule);
    passScheduleOut(newSchedule);
  }
  return (
    <Wrapper>
      <header>
        <H1>{header}</H1>
        <p>{subHeader}</p>
      </header>
      <br/>
      <ScheduleWrapper>
        <ScheduleSelector
          selection={schedule}
          startDate={new Date(startYear, startMonth-1, startDate)}
          numDays={num_days}
          minTime={min_time}
          maxTime={max_time}
          hourlyChunks={1}
          onChange={handleChange}
          timeFormat={"hh:mma"}
        />
      </ScheduleWrapper>
    </Wrapper>
  )
}

export default Schedular;