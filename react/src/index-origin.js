import React from "react"
import { render } from "react-dom"
import VoteCreate from "./components/VoteCreate"
import Banner from "./components/Banner"

const styles = {
    fontFamily: "sans-serif",
    textAlign: "center",
}


// render(<Banner />, document.querySelector("#banner"));
render(<VoteCreate textAlign="center" />, document.querySelector("#form"))
