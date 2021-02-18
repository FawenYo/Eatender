import React from 'react'
import { Paper, makeStyles } from "@material-ui/core"

import VoteCreateForm from "./VoteCreateForm";


const useStyles = makeStyles(theme => ({
    pageContent: {
        margin: theme.spacing(5),
        padding: theme.spacing(3),
    }
}))

function VoteCreate() {

    const classes = useStyles();

    return (
        <>
            <Paper className={classes.pageContent}>
                <VoteCreateForm />
            </Paper>  
        </>
    )
}

export default VoteCreate
