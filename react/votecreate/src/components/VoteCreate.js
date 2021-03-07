import React, { useState } from 'react'
import styled from "styled-components";
import { motion } from "framer-motion";
import { makeStyles } from '@material-ui/core/styles';
import { Step, Stepper, StepLabel, Button } from "@material-ui/core"
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
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  button: {
    marginTop: theme.spacing(3),
    width: 200,
  },
}));

const todayDate = new Date();

var defaultDueDate = {
  year: todayDate.getFullYear(),
  month: todayDate.getMonth() + 1,
  day: todayDate.getDay()
}

/* Parts to improve */
var PreservedFormValues = {
  voteName: '',
  dueDate: '',
  dueTime: '',
  selectedTime: null,
  dateRange: [],
  timeSession: [],
}

var today = new Date();

/* DateSelect */
function MultiDateSelect() {
  const [dateRange, setDateRange] = useState(PreservedFormValues.dateRange);

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

/* END OF DateSelect PART */

/* TimeSessioin Part */
const HeaderText_timeSelect = styled.h2`
    font-size: 24px;
    font-weight: 600 !important;
    line-height: 1;
    color: #000;
    z-index: 10;
    margin: 10;
`;

function TimeSessionSelect() {

  const handleOnClick = (e) => {
    const value = e.target.value;
    if (PreservedFormValues.timeSession.includes(value)) {
      PreservedFormValues.timeSession.pop(value);
    }
    else {
      PreservedFormValues.timeSession.push(value);
    }
  }

  return (
    <>
      <center>
        <HeaderText_timeSelect>選擇聚餐時段</HeaderText_timeSelect>
        <input type="checkbox" id="breakfast" value="早餐" onClick={handleOnClick} />
        <label for="breakfast">早餐</label>
        <input type="checkbox" id="lunch" value="午餐" onClick={handleOnClick} />
        <label for="lunch">午餐</label>
        <input type="checkbox" id="teatime" value="下午茶" onClick={handleOnClick} />
        <label for="teatime">下午茶</label>
        <input type="checkbox" id="dinner" value="晚餐" onClick={handleOnClick} />
        <label for="dinner">晚餐</label>
        <input type="checkbox" id="supper" value="宵夜" onClick={handleOnClick} />
        <label for="supper">宵夜</label>
      </center>
    </>
  );
}

/* END OF TimeSessioin Part */

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
  } = useForm(PreservedFormValues, true, validate);

  const HeaderText = styled.h2`
      font-size: 24px;
      font-weight: 600 !important;
      line-height: 1;
      color: #000;
      z-index: 10;
      margin: 10;
  `;

  /* Parts to improve */

  const [dueDate, setDueDate] = useState(defaultDueDate);


  const [selectedTime, setSelectedTime] = useState(PreservedFormValues.selectedTime);

  const parseTimeTo24h = () => {
    if (selectedTime) {
      PreservedFormValues.selectedTime = selectedTime;
      const temp = String(selectedTime);
      const re = /\d\d:\d\d/g;
      PreservedFormValues.dueTime = temp.match(re);
    }
  }
  const syncDueDateToPreserved = () => {
    parseTimeTo24h();
    if (dueDate && selectedTime && values.voteName) {
      PreservedFormValues.dueDate = `${dueDate.year}/${dueDate.month}/${dueDate.day} ${PreservedFormValues.dueTime}:00`;
      PreservedFormValues.voteName = values.voteName;

      defaultDueDate.year = dueDate.year
      defaultDueDate.month = dueDate.month
      defaultDueDate.day = dueDate.day
    }
  }
  syncDueDateToPreserved();
  PreservedFormValues.voteName = values.voteName ? values.voteName : "";

  /* END OF TODO PART */

  return (
    <Form>
      <center>
        <HeaderText>
          輸入聚餐名稱
        </HeaderText>
      </center>
      <Controls.Input
        name="voteName"
        label="聚餐名稱"
        value={values.voteName}
        onChange={handleInputChange}
        error={errors.voteName}
      />
      <center>
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
      </center>
    </Form>
  )
}

/* Control each steps content */
function getStepContent(step) {
  switch (step) {
    case 0:
      return <VoteName_DueDate />;
    case 1:
      return <MultiDateSelect />;
    case 2:
      return <TimeSessionSelect />;
    default:
      throw new Error('Unknown step');
  }
}

const steps = [`聚餐名稱＆截止日期`, `聚餐日期選擇`, '聚餐時段選擇'];

export default function VoteCreate() {

  const {
    values,
    setValues,
    errors,
    setErrors,
    handleInputChange,
    resetForm,
  } = useForm(PreservedFormValues, true)
  /* Submit Part */

  const [activeStep, setActiveStep] = React.useState(0);

  const classes = useStyles();

  /* SUBMIT */
  const handleSubmit = e => {
    let user_id;
    const query_url = new URL(window.location.href)
    if (query_url.searchParams.has("liff.state")) {
      const query_params = new URLSearchParams(query_url.searchParams.get("liff.state"))
      user_id = query_params.get("user_id")
    } else {
      user_id = query_url.searchParams.get("user_id")
    }
    const postedData = {
      "user_id": user_id,
      'vote_name': PreservedFormValues.voteName,
      'due_date': PreservedFormValues.dueDate,
      'date_range': PreservedFormValues.dateRange,
      'time_session': PreservedFormValues.timeSession,
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
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "很抱歉！",
          text: "無法連接伺服器，請稍後再試",
          confirmButtonText: "確認",
        });
      });
  }

  const handleNext = () => {
    if (activeStep == 0) {
      let validation = true;
      function checkVoteName() {
        const invalidCharacters = ["$", "@", "+", "＋"];
        if (PreservedFormValues.voteName) {
          if (invalidCharacters.some(invalidChar => PreservedFormValues.voteName.includes(invalidChar))) {
            validation = false;
            Swal.fire({
              icon: "error",
              title: "很抱歉！",
              text: "投票名稱不得含有'$', '@', '+'等非法字元",
              confirmButtonText: "確認",
            });
          }
        } else {
          validation = false;
          Swal.fire({
            icon: "error",
            title: "很抱歉！",
            text: "投票名稱不得為空",
            confirmButtonText: "確認",
          });
        }
      }
      function checkDueDate() {
        if (!PreservedFormValues.dueDate) {
          validation = false;
          Swal.fire({
            icon: "error",
            title: "很抱歉！",
            text: "投票截止日期與時間不得為空",
            confirmButtonText: "確認",
          });
        }
      }
      checkVoteName()
      if (validation) {
        checkDueDate()
        if (validation) {
          setActiveStep(activeStep + 1);
        }
      }
    } else if (activeStep == 1) {
      let validation = true;
      if (PreservedFormValues.dateRange.length == 0) {
        validation = false;
        Swal.fire({
          icon: "error",
          title: "很抱歉！",
          text: "聚餐日期不得為空",
          confirmButtonText: "確認",
        });
      }
      if (validation) {
        setActiveStep(activeStep + 1);
      }
    }
    if (activeStep === steps.length - 1) {
      let validation = true;
      if (PreservedFormValues.timeSession.length == 0) {
        validation = false;
        Swal.fire({
          icon: "error",
          title: "很抱歉！",
          text: "選擇聚餐時段不得為空",
          confirmButtonText: "確認",
        });
      }
      if (validation) {
        handleSubmit();
      }
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
                  <Button
                    variant="contained"
                    onClick={handleBack}
                    className={classes.button}
                  >
                    回上一步
                  </Button>
                )}
                <Button
                  variant="contained"
                  color="primary"
                  id="nextStepButton"
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
