import React, { useState } from "react"
import ReactDOM from "react-dom"
import RestaurantMenuIcon from '@material-ui/icons/RestaurantMenu';import Button from "@material-ui/core/Button"
import CssBaseline from "@material-ui/core/CssBaseline"
import TextField from "@material-ui/core/TextField"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import Checkbox from "@material-ui/core/Checkbox"
import Link from "@material-ui/core/Link"
import Grid from "@material-ui/core/Grid"
import Box from "@material-ui/core/Box"
import Typography from "@material-ui/core/Typography"
import { makeStyles } from "@material-ui/core/styles"
import InputLabel from "@material-ui/core/InputLabel"
import MenuItem from "@material-ui/core/MenuItem"
import ListSubheader from "@material-ui/core/ListSubheader"
import FormControl from "@material-ui/core/FormControl"
import Select from "@material-ui/core/Select"
import "react-modern-calendar-datepicker/lib/DatePicker.css"
import DatePicker from "react-modern-calendar-datepicker"

// imports from ./
import MultiDate from "./DateRange"

const Form = (props) => {
    const timeRangeStyles = makeStyles((theme) => ({
        formControl: {
            margin: theme.spacing(1),
            minWidth: 120,
        },
    }))
    const timeRangeClass = timeRangeStyles()

    const submitButtonStyle = makeStyles((theme) => ({
        button: {
            margin: theme.spacing(1),
        },
    }))
    const submitButtonClass = submitButtonStyle()

    const [selectedDay, setSelectedDay] = useState(null)

    // render regular HTML input element
    const renderCustomInput = ({ ref }) => (
        <input
            readOnly
            ref={ref} // necessary
            placeholder="設定投票截止日期"
            value={selectedDay ? `${selectedDay.year}年` + `${selectedDay.month}月` + `${selectedDay.day}日` : ""}
            style={{
                textAlign: "center",
                padding: "0.75rem 0.75rem",
                fontSize: "1.25rem",
                border: "1px solid #9c88ff",
                borderRadius: "50px",
                boxShadow: "0 0.25rem 0.25rem rgba(156, 136, 255, 0.2)",
                color: "#9c88ff",
                outline: "none",
            }}
            className="my-custom-input-class" // a styling class
        />
    )

    return (
        <React.Fragment>
            <React.Fragment>
                <Typography variant="h5">投票名稱</Typography>
                <TextField variant="outlined" margin="normal" required fullWidth id="Form" label="輸入投票名稱" />
            </React.Fragment>
            <React.Fragment>
                <Typography variant="h5">最早開始時間 / 最晚結束時間</Typography>
                <center>
                    <FormControl className={timeRangeClass.formControl} required>
                        <InputLabel htmlFor="grouped-select">最早時間</InputLabel>
                        <Select native defaultValue="" id="grouped-select">
                            <option aria-label="None" value="" />
                            <option value={0}>0 am</option>
                            <option value={1}>1 am</option>
                            <option value={2}>2 am</option>
                            <option value={3}>3 am</option>
                            <option value={4}>4 am</option>
                            <option value={5}>5 am</option>
                            <option value={6}>6 am</option>
                            <option value={7}>7 am</option>
                            <option value={8}>8 am</option>
                            <option value={9}>9 am</option>
                            <option value={10}>10 am</option>
                            <option value={11}>11 am</option>
                            <option value={12}>12 pm</option>
                            <option value={13}>13 pm</option>
                            <option value={14}>14 pm</option>
                            <option value={15}>15 pm</option>
                            <option value={16}>16 pm</option>
                            <option value={17}>17 pm</option>
                            <option value={18}>18 pm</option>
                            <option value={19}>19 pm</option>
                            <option value={20}>20 pm</option>
                            <option value={21}>21 pm</option>
                            <option value={22}>22 pm</option>
                            <option value={23}>23 pm</option>
                        </Select>
                    </FormControl>
                    <FormControl className={timeRangeClass.formControl} required>
                        <InputLabel htmlFor="grouped-select">最晚時間</InputLabel>
                        <Select native defaultValue="" id="grouped-select">
                            <option aria-label="None" value="" />
                            <option value={0}>0 am</option>
                            <option value={1}>1 am</option>
                            <option value={2}>2 am</option>
                            <option value={3}>3 am</option>
                            <option value={4}>4 am</option>
                            <option value={5}>5 am</option>
                            <option value={6}>6 am</option>
                            <option value={7}>7 am</option>
                            <option value={8}>8 am</option>
                            <option value={9}>9 am</option>
                            <option value={10}>10 am</option>
                            <option value={11}>11 am</option>
                            <option value={12}>12 pm</option>
                            <option value={13}>13 pm</option>
                            <option value={14}>14 pm</option>
                            <option value={15}>15 pm</option>
                            <option value={16}>16 pm</option>
                            <option value={17}>17 pm</option>
                            <option value={18}>18 pm</option>
                            <option value={19}>19 pm</option>
                            <option value={20}>20 pm</option>
                            <option value={21}>21 pm</option>
                            <option value={22}>22 pm</option>
                            <option value={23}>23 pm</option>
                        </Select>
                    </FormControl>
                </center>
            </React.Fragment>
            <React.Fragment>
                <Typography variant="h5">投票截止日期</Typography>
                <center>
                    <DatePicker
                        value={selectedDay}
                        onChange={setSelectedDay}
                        renderInput={renderCustomInput} // render a custom input
                        shouldHighlightWeekends
                    />
                </center>
            </React.Fragment>
            <React.Fragment>
                <Typography variant="h5">聚餐日期</Typography>
                <center>
                    <MultiDate />
                </center>
            </React.Fragment>
            <React.Fragment>
                <center>
                    <Button
                        variant="contained"
                        color="primary"
                        size="large"
                        className={submitButtonClass.button}
                        endIcon={<RestaurantMenuIcon />}
                    >
                        建立投票
                    </Button>
                </center>
            </React.Fragment>
        </React.Fragment>
    )
}

export default Form
