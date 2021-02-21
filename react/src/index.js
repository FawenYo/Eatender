import React from "react"
import { render } from "react-dom"
import VoteCreate from "./components/VoteCreate"

const styles = {
    fontFamily: "sans-serif",
    textAlign: "center",
}


render(<VoteCreate textAlign="center" />, document.querySelector("#form"))
