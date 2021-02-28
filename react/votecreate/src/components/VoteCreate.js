import React, { useState } from 'react'
import styled from "styled-components";
import { motion } from "framer-motion";
import { makeStyles, useTheme } from '@material-ui/core/styles';
import { AppBar, CssBaseline, Step, Stepper, StepLabel, Button, Typography } from "@material-ui/core"
import { Chip, FormControl, MenuItem, Select, InputLabel, Input } from '@material-ui/core';
import VoteName_DueDate from "./Name_Date";
import { useForm, Form } from "./useForm";

// ./ imports
import Controls from "./controls/Controls";

// To be improved
import 'react-modern-calendar-datepicker/lib/DatePicker.css';
import DatePicker, { Calendar, utils } from 'react-modern-calendar-datepicker';
import { NoEncryption, SentimentSatisfiedAlt } from '@material-ui/icons';
import Swal from 'sweetalert2';

const AppContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const BoxContainer = styled.div`
  width: 330px;
  min-height: 550px;
  display: flex;
  flex-direction: column;
  border-radius: 19px;
  background-color: #fff;
  box-shadow: 0 0 2px rgba(15, 15, 15, 0.28);
  position: relative;
  overflow: hidden;
`;

const TopContainer = styled.div`
  width: 100%;
  height: 185px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0 1.8em;
  padding-bottom: 5em;
`;

const AppBarContainer = styled.div`
  width: 100%;
  height: 65px;
  display: flex;
  justify-content: flex-end;
  padding: 1 0em;
`;

const HeaderContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
`;

const BannerText = styled.h2`
  font-size: 40px;
  font-weight: 600;
  line-height: 1.25;
  color: #fff;
  z-index: 10;
  margin: 0;
`;

const HeaderText = styled.h2`
  font-size: 30px;
  font-weight: 600;
  line-height: 1.25;
  color: #fff;
  z-index: 10;
  margin: 0;
`;

const SmallText = styled.h5`
  color: #c24510;
  font-weight: 1000 !important;
  font-size: 13px;
  z-index: 10;
  margin: 0;
  margin-top: 7px;
`;

const BackDrop = styled(motion.div)`
  width: 140%;
  height: 550px;
  position: absolute;
  display: flex;
  flex-direction: column;
  border-radius: 50%;
  transform: rotate(60deg);
  top: -290px;
  left: -70px;
  background: rgb(241, 196, 15);
  background: linear-gradient(
    58deg,
    rgba(250, 215, 87, 1) 20%,
    rgba(243, 172, 18, 1) 100%
  );
`;

const useStyles = makeStyles(theme => ({
  pageContent: {
    margin: theme.spacing(5),
    padding: theme.spacing(3),
  },
  appBar: {
    position: 'relative',
  },
  layout: {
    width: 'auto',
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(2) * 2)]: {
      width: 600,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
    padding: theme.spacing(2),
    [theme.breakpoints.up(600 + theme.spacing(3) * 2)]: {
      marginTop: theme.spacing(6),
      marginBottom: theme.spacing(6),
      padding: theme.spacing(3),
    },
  },
  stepper: {
    padding: theme.spacing(3, 0, 5),
    color: "rgba(241, 196, 15, 0.8)"
  },
  buttons: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  button: {
    marginTop: theme.spacing(3),
    marginLeft: theme.spacing(1),
  },
}));

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
  voteName: '',
  dueDate: '',
  dateRange: [],
  timeSession: [],
}

var today = new Date();

/* DateSelect */
function MultiDateSelect(){
  const [dateRange, setDateRange] = useState([]);
  
  const HeaderText = styled.h2`
    font-size: 24px;
    font-weight: 600 !important;
    line-height: 1;
    color: #000;
    z-index: 10;
    margin: 10;
  `;

  const updateToPreserved = () => {
    PreservedFormValues.dateRange = dateRange;
  }
  updateToPreserved();

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
    </>
  )
}

/* END OF TODO PART */

/* TimeSessioin Part */
const useStyles_timeSession = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
    maxWidth: 300,
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: 2,
  },
  noLabel: {
    marginTop: theme.spacing(3),
  },
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const names = [
  "早餐",
  "午餐",
  "下午茶",
  "晚餐",
  "宵夜",
];

function getStyles(name, timeSession, theme) {
  return {
    fontWeight:
      timeSession.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

const HeaderText_timeSelect = styled.h2`
    font-size: 24px;
    font-weight: 600 !important;
    line-height: 1;
    color: #000;
    z-index: 10;
    margin: 10;
`;

function TimeSessionSelect() {
  const classes = useStyles_timeSession();
  const theme = useTheme();
  const [timeSession, setTimeSession] = React.useState([]);

  const handleChange = (event) => {
    setTimeSession(event.target.value);
  };

  const handleChangeMultiple = (event) => {
    const { options } = event.target;
    const value = [];
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    setTimeSession(value);
  };

  const updateToPreserved = () => {
    PreservedFormValues.timeSession = timeSession;
  }
  updateToPreserved();

return (
    <>
    <center>
        <HeaderText_timeSelect>選擇聚餐時段</HeaderText_timeSelect>
    </center>
    <FormControl className={classes.formControl}>
    <InputLabel id="demo-mutiple-chip-label">選擇聚餐時段</InputLabel>
    <Select
        labelId="demo-mutiple-chip-label"
        id="demo-mutiple-chip"
        multiple
        variant="filled"
        value={timeSession}
        onChange={handleChange}
        input={<Input id="select-multiple-chip" />}
        renderValue={(selected) => (
        <div className={classes.chips}>
            {selected.map((value) => (
            <Chip 
              key={value} 
              label={value} 
              className={classes.chip}
              color="secondary"
            />
            ))}
        </div>
        )}
        MenuProps={MenuProps}
    >
        {names.map((name) => (
        <MenuItem key={name} value={name} style={getStyles(name, timeSession, theme)}>
            {name}
        </MenuItem>
        ))}
    </Select>
    </FormControl>
    </>
  );
}

const steps = [`聚餐名稱＆截止日期`, `聚餐日期選擇`, '聚餐時段選擇'];

function getStepContent(step) {
  switch (step) {
    case 0:
      return <VoteName_DueDate />;
    case 1:
      try {
        PreservedFormValues.voteName = document.getElementById("voteName").value;
        PreservedFormValues.dueDate = document.getElementById("dueDate").value;
      }
      catch (e) {}
      return <MultiDateSelect />;
    case 2:
      return <TimeSessionSelect />;
    default:
      throw new Error('Unknown step');
  }
}

export default function VoteCreate() {

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
} = useForm(initialFormValues, true)
/* Submit Part */

  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(0);

  /* SUBMIT */
  const handleSubmit = e => {
    const postedData = {
        "user_id": user_id,
        'vote_name': PreservedFormValues.voteName,
        'due_date': PreservedFormValues.dueDate,
        'date_range': PreservedFormValues.dateRange,
        'time_session': PreservedFormValues.timeSession,
    };
    // console.log(postedData);

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
  
  const handleNext = () => {
    setActiveStep(activeStep + 1);
    if (activeStep === steps.length - 1) {
      handleSubmit();
    }
  };
  
  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };
  
  return (
    <AppContainer>
      <BoxContainer>
        <TopContainer>
          <BackDrop
            initial={false}
          />
          <HeaderContainer>
            <BannerText>EATender</BannerText>
            <HeaderText>聚餐創立</HeaderText>
            <SmallText>加LINE約吃飯，感情不會散！</SmallText>
          </HeaderContainer>
        </TopContainer>
        <AppBarContainer>
          <Stepper activeStep={activeStep} className={classes.stepper}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </AppBarContainer>
        <React.Fragment>
            {activeStep === steps.length ? (
              <center>
                <HeaderText_timeSelect>
                  已建立聚餐投票
                </HeaderText_timeSelect>
                <HeaderText_timeSelect>
                  預祝 聚餐愉快(*´∀`)~♥
                </HeaderText_timeSelect>
              </center>
            ) : (
              <React.Fragment>
                {getStepContent(activeStep)}
                <div className={classes.buttons}>
                  {activeStep !== 0 && (
                    <Button onClick={handleBack} className={classes.button}>
                      回上一步
                    </Button>
                  )}
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                    className={classes.button}
                  >
                    {activeStep === steps.length - 1 ? '建立投票' : `前往${steps[activeStep + 1]}`}
                  </Button>
                </div>
              </React.Fragment>
            )}
          </React.Fragment>
      </BoxContainer>
    </AppContainer>
  )
}
