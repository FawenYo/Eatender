import React, { useState } from "react";
import "react-modern-calendar-datepicker/lib/DatePicker.css";
import { Calendar } from "react-modern-calendar-datepicker";

const MultiDate = () => {
  const defaultFrom = {
    year: 2021,
    month: 2,
    day: 7,
  };
  const defaultTo = {
    year: 2019,
    month: 2,
    day: 15,
  };
  const defaultValue = {
    from: defaultFrom,
    to: defaultTo,
  };
  const [selectedDayRange, setSelectedDayRange] = useState(
    defaultValue
  );

  return (
    <Calendar
      value={selectedDayRange}
      onChange={setSelectedDayRange}
      colorPrimary="#0fbcf9" // added this
      colorPrimaryLight="rgba(75, 207, 250, 0.4)" // and this
      shouldHighlightWeekends
    />
  );
};

export default MultiDate;