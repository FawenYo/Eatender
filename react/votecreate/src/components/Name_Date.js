import React, { useState } from 'react';
import styled from "styled-components";
import { Grid, TextField, makeStyles } from '@material-ui/core';
import { useForm, Form } from "./useForm";

// ./ imports
import Controls from "./controls/Controls";

// To be improved
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import { Calendar, utils } from 'react-modern-calendar-datepicker';
import Swal from 'sweetalert2';
import 'date-fns';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
} from '@material-ui/pickers';

const initialFormValues = {
    voteName: '',
    earliestTime: '',
    latestTime: '',
}

/* Parts to improve */
var PreservedFormValues = {
    dueDate: '',
    dueTime: '',
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
            const invalidCharacters = ["$", "@", "+", "＋"];
            if (!fieldValues.voteName) {
                temp.voteName = "請輸入投票名稱";
            }
            else if (invalidCharacters.some(invalidChar => fieldValues.voteName.includes(invalidChar))) {
                temp.voteName = "投票名稱不得含有'$', '@', '+'等非法字元";
            }
            else {
                temp.voteName = "";
            }
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

    const [selectedTime, setSelectedTime] = useState(null);

    const parseTimeTo24h = () => {
        if (selectedTime) {
            const temp = String(selectedTime)
            const re = /\d\d:\d\d/g;
            PreservedFormValues.dueTime = temp.match(re);
        }
    }
    parseTimeTo24h();

    /* END OF TODO PART */

    return (
        <Form>
            <center>
                <HeaderText>
                    輸入聚餐名稱
                </HeaderText>
                <Controls.Input
                    name="voteName"
                    label="聚餐名稱"
                    value={values.voteName}
                    onChange={handleInputChange}
                    error={errors.voteName}
                />
                <HeaderText>
                    投票截止日期＆時間
                </HeaderText>
                <Calendar
                    name="dueDate"
                    value={dueDate}
                    onChange={setDueDate}
                    shouldHighlightWeekends
                    minimumDate={utils().getToday()}
                />
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <KeyboardTimePicker
                        margin="normal"
                        id="time-picker"
                        label="投票截止時間"
                        value={selectedTime}
                        onChange={setSelectedTime}
                        KeyboardButtonProps={{
                            'aria-label': 'change time',
                        }}
                    />
                </MuiPickersUtilsProvider>
                <input style={{display: "none"}} id="voteName" value={values.voteName} />
                <input style={{display: "none"}} id="dueDate" value={PreservedFormValues.dueDate} />
                <input style={{display: "none"}} id="dueTime" value={PreservedFormValues.dueTime} />
            </center>
        </Form>
    )
}

export default VoteName_DueDate
