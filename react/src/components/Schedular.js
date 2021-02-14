import ScheduleSelector from 'react-schedule-selector';
import styled from 'styled-components';
import React, {useState} from 'react';

// 在要使用 schedular 的 js 檔中直接插入元件，並加入
// "總天數" "開始時間" "結束時間" 等參數，以及一個取得 schedule 的 callback。舉例如下： 
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


function Schedular({_numDays, _minTime, _maxTime, passScheduleOut}) {
  const [schedule, setSchedule] = useState([]);

  function handleChange(newSchedule) {
    setSchedule(newSchedule);
    passScheduleOut(newSchedule);
  }
  return (
    <Wrapper>
      <header>
        <H1>React Schedule Selector</H1>
        <p>Tap to select one time or drag to select multiple times at once.</p>
      </header>
      <br/>
      <ScheduleWrapper>
        <ScheduleSelector
          selection={schedule}
          numDays={_numDays}
          minTime={_minTime}
          maxTime={_maxTime}
          hourlyChunks={1}
          onChange={handleChange}
          timeFormat={"hh:mma"}
        />
      </ScheduleWrapper>
    </Wrapper>
  )
}

export default Schedular;