import React from 'react'
import ReactDOM from 'react-dom'
import Schedular from './components/Schedular'

ReactDOM.render(
  <React.StrictMode>
    <Schedular
      _startDate = {new Date()}
      _numDays = {5}
      _minTime = {8}
      _maxTime = {22}
      passScheduleOut = {schedule => console.log(schedule)}
    />
  </React.StrictMode>,
  document.getElementById('schedular')
)

