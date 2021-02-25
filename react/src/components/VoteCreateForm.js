import React, { useState } from 'react';
import { Grid, TextField, makeStyles } from '@material-ui/core';
import { useForm, Form } from "./useForm";

// ./ imports
import Controls from "./controls/Controls";

// To be improved
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import DatePicker, { Calendar, utils } from 'react-modern-calendar-datepicker';
import { SentimentSatisfiedAlt } from '@material-ui/icons';

let user_id;

$(document).ready(function () {

    const query_url = new URL(window.location.href)
    if (query_url.searchParams.has("liff.state")) {
        const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))
        user_id = query_params.get("user_id")
    } else {
        user_id = query_url.searchParams.get("user_id")
    }
})

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
            temp.earliestTime = fieldValues.earliestTime.length != 0 ? "" : "請選擇聚餐最早開始時間";
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


    /* Submit Part */

    const handleSubmit = e => {
        e.preventDefault();

        if (!validate()) { return; }

        // Parsing local data
        const date1 = new Date(PreservedFormValues.dateRange.startDate);
        const startDate = `${date1.getFullYear()}/${date1.getMonth() + 1}/${date1.getDate()}`
        const date2 = new Date(PreservedFormValues.dateRange.endDate);
        const diffInTime = date2.getTime() - date1.getTime();
        const diffInDays = (diffInTime / (1000 * 3600 * 24)) + 1;



        const postedData = {
            "user_id": user_id,
            'vote_name': values.voteName,
            'vote_end': PreservedFormValues.dueDate,
            'start_date': startDate,
            'num_days': diffInDays,
            'min_time': values.earliestTime,
            'max_time': values.latestTime,
        };

        const requestOptions = {
            method: 'POST',
            header: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postedData),
            mode: 'cors'
        };
        fetch('../api/vote/create/event', requestOptions)
            .then(response => response.json())
            .then((data) => {
                if (data && data.status === "success") {
                    Swal.fire({
                        icon: "success",
                        title: data.message.title,
                        text: data.message.content,
                        confirmButtonText: "確認",
                    }).then((result) => {
                        window.location.replace(data.message.share_link);
                    });
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "很抱歉！",
                        text: data.error_message,
                        confirmButtonText: "確認",
                    });
                }
            });
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
                padding: "0.75rem 0.5rem",
                fontSize: "1.25rem",
                border: "1px solid #808080",
                borderRadius: "50px",
                // boxShadow: "0 0.25rem 0.25rem rgba(156, 136, 255, 0.2)",
                color: "#f1c40f",
                outline: "none",
            }}
        />
    )


    const syncDueDateToPreserved = () => {
        if (dueDate) {
            PreservedFormValues.dueDate = `${dueDate.month}/${dueDate.day}/${dueDate.year}`;
        }
    }
    syncDueDateToPreserved();

    const defaultDateRange = {
        from: utils().getToday(),
        to: null,
    };
    const [dateRange, setDateRange] = useState(defaultDateRange)
    const syncDateRangeToPreserved = () => {
        if (dateRange.from !== null && dateRange.to !== null) {
            PreservedFormValues.dateRange.startDate = `${dateRange.from.month}/${dateRange.from.day}/${dateRange.from.year}`;
            PreservedFormValues.dateRange.endDate = `${dateRange.to.month}/${dateRange.to.day}/${dateRange.to.year}`;
        }
    }
    syncDateRangeToPreserved();

    const checkValidation = () => {
        if (
            values.voteName.length != 0 &&
            Number.isInteger(values.earliestTime) &&
            Number.isInteger(values.latestTime) &&
            PreservedFormValues.dueDate.length != 0 &&
            PreservedFormValues.dateRange.startDate.length != 0 &&
            PreservedFormValues.dateRange.endDate.length != 0
        ) { return false; }
        return true;
    }

    /* END OF TODO PART */

    return (
        <Form onSubmit={handleSubmit}>
            <center>
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
                    minimumDate={utils().getToday()}
                    shouldHighlightWeekends
                />
                <h2>投票聚餐日期</h2>
                <Calendar
                    value={dateRange}
                    onChange={setDateRange}
                    colorPrimary="#f1c40f"
                    colorPrimaryLight="rgba(241, 196, 15, 0.2)"
                    minimumDate={utils().getToday()}
                    shouldHighlightWeekends
                />
                <div>
                    <Controls.Button
                        type="submit"
                        text="建立投票"
                        disabled={checkValidation()}
                    />
                    {/* <Controls.Button 
                        text="重置投票"
                        color="default"
                        onClick={resetForm}
                    /> */}
                </div>
            </center>

            {/* <li>Returned Id: {postId}</li>
            <li>聚餐名稱: {values.voteName}</li>
            <li>最早時間: {values.earliestTime}</li>
            <li>最晚時間: {values.latestTime}</li>
            <li>截止日期: {PreservedFormValues.dueDate}</li>
            <li>投票日期: {PreservedFormValues.dateRange.startDate}~{PreservedFormValues.dateRange.endDate}</li> */}
        </Form>
    )
}

export default VoteCreateForm
