import React, { useState } from 'react';
import styled from "styled-components";
import { Grid, TextField, makeStyles, Typography } from '@material-ui/core';
import { useForm, Form } from "./useForm";
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import { Calendar, utils } from 'react-modern-calendar-datepicker';

var today = new Date();

export default function MultiDateSelect(){

    const HeaderText = styled.h2`
        font-size: 24px;
        font-weight: 600 !important;
        line-height: 1;
        color: #000;
        z-index: 10;
        margin: 10;
    `;

    const preselectedDays = [
        {
          year: today.getFullYear(),
          month: today.getMonth() + 1,
          day: today.getDate(),
        },
    ]

    const [dateRange, setDateRange] = useState([]);
    console.log(dateRange)

    /* END OF TODO PART */

    return (
        <>
        <Form>
            <center>
                <HeaderText>
                    選擇聚餐日期
                </HeaderText>
                <Calendar
                    name="dateRange"
                    value={dateRange}
                    onChange={setDateRange}
                    shouldHighlightWeekends
                    minimumDate={utils().getToday()}
                />
            </center>
        </Form>
        <input style={{display: "none"}} id="dateRange" value={dateRange} />
        </>
    )
}
