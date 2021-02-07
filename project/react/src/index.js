import React from "react"
import { render } from "react-dom"
import Form from "./components/Form"
import Banner from "./components/Banner"

const styles = {
    fontFamily: "sans-serif",
    textAlign: "center",
}

const DateTimes = () => (
    <div style={styles}>
        <DateRange />
    </div>
)

// render(<Banner />, document.querySelector("#banner"));
render(<Form textAlign="center" />, document.querySelector("#form"))
