import React, { useState } from "react"
import "react-modern-calendar-datepicker/lib/DatePicker.css"
import { Calendar } from "react-modern-calendar-datepicker"

const DateRange = () => {
    var current = new Date();
    const defaultFrom = {
        year: current.getFullYear(),
        month: current.getMonth(),
        day: current.getDate(),
    }
    const defaultValue = {
        from: defaultFrom,
        to: null,
    }
    const [selectedDayRange, setSelectedDayRange] = useState(defaultValue)

    return (
        <Calendar
            value={selectedDayRange}
            onChange={setSelectedDayRange}
            colorPrimary="#0fbcf9" // added this
            colorPrimaryLight="rgba(75, 207, 250, 0.4)" // and this
            shouldHighlightWeekends
        />
    )
}

export default DateRange
