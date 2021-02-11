import ScheduleSelector from 'react-schedule-selector';
import React, {useState} from 'react';

// 在要使用 schedular 的 js 檔中直接插入元件，並加入
// "總天數" "開始時間" "結束時間" 等參數，以及一個取得 schedule 的 callback。如下： 
// 
//  <Schedular
//    _startDate = {new Date()}
//    _numDays = {5}
//    _minTime = {8}
//    _maxTime = {22}
//    passScheduleOut = {getSchedule}
//  ></Schedular>
// 
// getSchedule 會在使用者按下確認按鈕後被呼叫，其中 arguments 為 schedule。
// getSchedule 需要在使用到 Schedular 的 js 檔中自行定義。
//
// 簡單的 getSchedule 範例：
// 
//  function getSchedule(schedule){ 
//    console.log(schedule); 
//  }
//
function Schedular({_startDate, _numDays, _minTime, _maxTime, passScheduleOut}) {
  const [schedule, setSchedule] = useState([]);

  function handleChange(newSchedule) {setSchedule(newSchedule)};

  return (
    <div style={{textAlign: "center", margin: "0 auto", width:"80%"}}>
      <header>
        <h1>React Schedule Selector</h1>
        <p>Tap to select one time or drag to select multiple times at once.</p>
        <button 
          style={{
            minWidth: "50px", maxWidth: "200px", width: "10%",
            minHeight: "30px", maxWidth: "120px", width: "6%"
          }} 
          onClick={()=>passScheduleOut(schedule)}>確認</button>
      </header>
      <br/>
      <div
        style={{
          padding: "20px",
          borderRadius: "20px",
          boxShadow: "3px 5px 18px 0px rgba(191,191,191,0.76)"
        }}>
        <ScheduleSelector
          selection={schedule}
          startDate={_startDate}
          numDays={_numDays}
          minTime={_minTime}
          maxTime={_maxTime}
          hourlyChunks={1}
          onChange={handleChange}
          timeFormat={"hh:mma"}
        />
      </div>
    </div>
  )
}

export default Schedular;