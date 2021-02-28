import React, { useState } from 'react';
import styled from "styled-components";
import { Grid, TextField, makeStyles } from '@material-ui/core';
import { useForm, Form } from "./useForm";

// ./ imports
import Controls from "./controls/Controls";

// To be improved
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import { Calendar, utils } from 'react-modern-calendar-datepicker';
import { SentimentSatisfiedAlt } from '@material-ui/icons';
import Swal from 'sweetalert2';

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

function VoteName_DueDate() {

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

    const HeaderText = styled.h2`
        font-size: 24px;
        font-weight: 600 !important;
        line-height: 1;
        color: #000;
        z-index: 10;
        margin: 10;
    `;

    /* Parts to improve */

    const [dueDate, setDueDate] = useState(utils().getToday());

    const syncDueDateToPreserved = () => {
        if (dueDate) {
            PreservedFormValues.dueDate = `${dueDate.year}/${dueDate.month}/${dueDate.day}`;
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
                <HeaderText>
                    輸入聚餐名稱＆截止日期
                </HeaderText>
                <Controls.Input
                    name="voteName"
                    label="聚餐名稱"
                    value={values.voteName}
                    onChange={handleInputChange}
                    error={errors.voteName}
                />
                <Calendar
                    name="dueDate"
                    value={dueDate}
                    onChange={setDueDate}
                    shouldHighlightWeekends
                    minimumDate={utils().getToday()}
                />
                <input style={{display: "none"}} id="voteName" value={values.voteName} />
                <input style={{display: "none"}} id="dueDate" value={PreservedFormValues.dueDate} />
            </center>
        </Form>
    )
}

export default VoteName_DueDate
