import React from 'react'
import { TextField } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

export default function Input(props) {

    const useStyles = makeStyles(theme => ({
        inputBox: {
            width: "95% !important",
        },
    }));
    const classes = useStyles();
    const { name, label, value, onChange, error = null } = props;
    return (
        <TextField
            className={classes.inputBox}
            variant="outlined"
            name={name}
            label={label}
            value={value}
            onChange={onChange}
            // required
            {...(error && { error: true, helperText: error })}
        />
    )
}
