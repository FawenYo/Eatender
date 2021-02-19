import React, { useState } from 'react'
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import { DatePicker as ModernDatePicker } from 'react-modern-calendar-datepicker';

export default function DatePicker(props) {

    const { name, value, onChange, inputPlaceholder, inputClassName } = props
    const formatInputValue = () => {
        if (!value) return '';
        return `Day: ${value.day}`;
    };
      return (
        <ModernDatePicker
            value={selectedDay}
            onChange={setSelectedDay}
            inputPlaceholder="Select a date" // placeholder
            formatInputText={formatInputValue} // format value
            inputClassName="my-custom-input" // custom class
            shouldHighlightWeekends
        />
    );
}
