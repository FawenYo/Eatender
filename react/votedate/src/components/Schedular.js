import ScheduleSelector from 'react-schedule-selector';
import styled from 'styled-components';
import React, { useState } from 'react';

const Wrapper = styled.div`
  text-align: center;
  margin: 0 auto;
  width: 80%;`

const ScheduleWrapper = styled.div`
  padding: 20px;
  border-radius: 20px;
  background: white;
  box-shadow: 3px 5px 18px 0px rgba(191,191,191,0.76);`

const H1 = styled.h1`
  font-size: 32pt;`


function Schedular({ header, subHeader, startYear, startMonth, startDate, num_days, min_time, max_time, passScheduleOut, lastSelect }) {
  const [schedule, setSchedule] = useState(lastSelect);

  function handleChange(newSchedule) {
    setSchedule(newSchedule);
    passScheduleOut(newSchedule);
  }
  return (
    <Wrapper>
      <header>
        <H1>{header}</H1>
        <p>{subHeader}</p>
        <p>拖曳或點擊以選擇時間</p>
      </header>
      <br />
      <ScheduleWrapper>
        <ScheduleSelector
          selection={schedule}
          startDate={new Date(startYear, startMonth - 1, startDate)}
          numDays={num_days}
          minTime={min_time}
          maxTime={max_time}
          hourlyChunks={1}
          onChange={handleChange}
          timeFormat={"hh:mma"}
          hoveredColor="rgb(219, 237, 255)"
        />
      </ScheduleWrapper>
    </Wrapper>
  )
}

export default Schedular;