import React from 'react'
import { makeStyles, FormControl, InputLabel, Select, MenuItem, FormHelperText } from '@material-ui/core'

function TimeRange(props) {

    const useStyle = makeStyles((theme) => ({
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
    }))
    const useClasses = useStyle();

    const [timeSession, setTimeSession] = useState(null)

    return (
        <FormControl
            style={{minWidth: 120}}
            variant="standard"
            margin="normal"
            // required 
            {...(error && { error: true })}
        >
            <InputLabel>{label}</InputLabel>
            <Select
                defaultValue=""
                label="選擇聚餐時段"
                value={timeSession}
                onChange={setTimeSession}
                autoWidth={true}
            >
                <MenuItem value={0}>0 am</MenuItem>
                <MenuItem value={1}>1 am</MenuItem>
                <MenuItem value={2}>2 am</MenuItem>
                <MenuItem value={3}>3 am</MenuItem>
                <MenuItem value={4}>4 am</MenuItem>
                <MenuItem value={5}>5 am</MenuItem>
                <MenuItem value={6}>6 am</MenuItem>
                <MenuItem value={7}>7 am</MenuItem>
                <MenuItem value={8}>8 am</MenuItem>
                <MenuItem value={9}>9 am</MenuItem>
                <MenuItem value={10}>10 am</MenuItem>
                <MenuItem value={11}>11 am</MenuItem>
                <MenuItem value={12}>12 pm</MenuItem>
                <MenuItem value={13}>13 pm</MenuItem>
                <MenuItem value={14}>14 pm</MenuItem>
                <MenuItem value={15}>15 pm</MenuItem>
                <MenuItem value={16}>16 pm</MenuItem>
                <MenuItem value={17}>17 pm</MenuItem>
                <MenuItem value={18}>18 pm</MenuItem>
                <MenuItem value={19}>19 pm</MenuItem>
                <MenuItem value={20}>20 pm</MenuItem>
                <MenuItem value={21}>21 pm</MenuItem>
                <MenuItem value={22}>22 pm</MenuItem>
                <MenuItem value={23}>23 pm</MenuItem>
            </Select>
            {error && <FormHelperText>{error}</FormHelperText>}
        </FormControl>
    )
}

export default TimeRange
