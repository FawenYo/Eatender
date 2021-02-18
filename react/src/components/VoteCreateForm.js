import React, { useState, useEffect } from 'react';
import { Grid, TextField, makeStyles } from '@material-ui/core';
import { useForm, Form } from "./useForm";

// ./ imports
import Controls from "./controls/Controls";

// To be improved
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import DatePicker, { Calendar } from 'react-modern-calendar-datepicker';

const initialFormValues = {
    voteName: '',
    earliestTime: '',
    latestTime: '',
}

/* Parts to improve */
var PreservedFormValues = {
    dueDate: '',
    dateRange: {
        startDate: '',
        endDate: '',
    }
}

/* END OF TODO PART */

function VoteCreateForm() {

    /* Error report */
    const validate = (fieldValues = values) => {
        let temp = { ...errors }
        if ('voteName' in fieldValues) {
            temp.voteName = fieldValues.voteName ? "" : "請輸入投票名稱";
        }
        if ('earliestTime' in fieldValues) {
            temp.earliestTime = fieldValues.earliestTime.length != 0? "" : "請選擇聚餐最早開始時間";
        }
        if ('latestTime' in fieldValues) {
            temp.latestTime = fieldValues.latestTime.length != 0 ? "" : "請選擇聚餐最晚結束時間";
        }
        if (Number.isInteger(fieldValues.earliestTime) && 
                Number.isInteger(fieldValues.latestTime)) {
            temp.latestTime = fieldValues.earliestTime >= fieldValues.latestTime ? "最晚時間需要比最早時間晚" : "";
        }
        setErrors({
            ...temp
        })    
        if (fieldValues == values)
            return Object.values(temp).every(x => x == "")
    }

    const {
        values,
        setValues,
        errors,
        setErrors,
        handleInputChange,
        resetForm,
    } = useForm(initialFormValues, true, validate);

    const handleSubmit = e => {
        e.preventDefault()
        if (validate()){
            resetForm()
        }
    }

    /* Parts to improve */

    const [dueDate, setDueDate] = useState(null);
    // 投票截止日期的css和init
    const renderCustomInput = ({ ref }) => (
        <input
            readOnly
            ref={ref} // necessary
            placeholder="設定投票截止日期"
            value={dueDate ? `${dueDate.year}年` + `${dueDate.month}月` + `${dueDate.day}日` : ""}
            style={{
                textAlign: "center",
                padding: "0.75rem 0.75rem",
                fontSize: "1.25rem",
                // border: "1px solid #9c88ff",
                borderRadius: "50px",
                // boxShadow: "0 0.25rem 0.25rem rgba(156, 136, 255, 0.2)",
                // color: "#9c88ff",
                outline: "none",
            }}
        />
    )

    
    const syncDueDateToPreserved = () => {
        if (dueDate) {
            PreservedFormValues.dueDate = `${dueDate.year}/${dueDate.month}/${dueDate.day}`;
        }
    }
    syncDueDateToPreserved();

    // 選定欲投票的日期範圍
    let current = new Date();
    const defaultFrom = {
        year: current.getFullYear(),
        month: current.getMonth(),
        day: current.getDate(),
    }
    const defaultValue = {
        from: defaultFrom,
        to: null,
    }
    const [dateRange, setDateRange] = useState(defaultValue)
    const syncDateRangeToPreserved = () => {
        if (dateRange.from !== null && dateRange.to !== null) {
            PreservedFormValues.dateRange.startDate = `${dateRange.from.year}/${dateRange.from.month}/${dateRange.from.day}`;
            PreservedFormValues.dateRange.endDate = `${dateRange.to.year}/${dateRange.to.month}/${dateRange.to.day}`;
        }
    }
    syncDateRangeToPreserved();
    
    /* END OF TODO PART */

    return (
        <Form onSubmit={handleSubmit}>
            <Controls.Input
                name="voteName"
                label="聚餐名稱"
                value={values.voteName}
                onChange={handleInputChange}
                error={errors.voteName}
            />
            <div>
                <Controls.TimeRange 
                    name="earliestTime"
                    label="聚餐最早開始時間"
                    value={values.earliestTime}
                    onChange={handleInputChange}
                    error={errors.earliestTime}
                />
                <Controls.TimeRange 
                    name="latestTime"
                    label="聚餐最晚結束時間"
                    value={values.latestTime}
                    onChange={handleInputChange}
                    error={errors.latestTime}
                />
            </div>
            <DatePicker
                name="dueDate"
                value={dueDate}
                onChange={setDueDate}
                renderInput={renderCustomInput}
                shouldHighlightWeekends
            />
            <h2>投票聚餐日期</h2>
            <Calendar
                value={dateRange}
                onChange={setDateRange}
                colorPrimary="#0fbcf9" // added this
                colorPrimaryLight="rgba(75, 207, 250, 0.4)" // and this
                shouldHighlightWeekends
            />
            <div>
                <Controls.Button 
                    type="submit"
                    text="建立投票"
                />
                <Controls.Button 
                    text="重置投票"
                    color="default"
                    onClick={resetForm}
                />
            </div>

            <li>聚餐名稱: {values.voteName}</li>
            <li>最早時間: {values.earliestTime}</li>
            <li>最晚時間: {values.latestTime}</li>
            <li>截止日期: {PreservedFormValues.dueDate}</li>
            <li>投票日期: {PreservedFormValues.dateRange.startDate}~{PreservedFormValues.dateRange.endDate}</li>
        </Form>
    )
}

export default VoteCreateForm
