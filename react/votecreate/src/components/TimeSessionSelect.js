import React from 'react';
import styled from "styled-components";
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';

const useStyles = makeStyles((theme) => ({
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

    const HeaderText = styled.h2`
        font-size: 24px;
        font-weight: 600 !important;
        line-height: 1;
        color: #000;
        z-index: 10;
        margin: 10;
    `;

export default function TimeSessionSelect() {
  const classes = useStyles();
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
    console.log(timeSession);


return (
    <>
    <center>
        <HeaderText>選擇聚餐時段</HeaderText>
    </center>
    <FormControl className={classes.formControl}>
    <InputLabel id="demo-mutiple-chip-label">選擇聚餐時段</InputLabel>
    <Select
        labelId="demo-mutiple-chip-label"
        id="demo-mutiple-chip"
        multiple
        value={timeSession}
        onChange={handleChange}
        input={<Input id="select-multiple-chip" />}
        renderValue={(selected) => (
        <div className={classes.chips}>
            {selected.map((value) => (
            <Chip key={value} label={value} className={classes.chip} />
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
