import React, { useEffect, useState } from "react";
import Faker from "faker";
import Assessment from "@material-ui/icons/Assessment";
import GridOn from "@material-ui/icons/GridOn";
import PermIdentity from "@material-ui/icons/PermIdentity";
import Web from "@material-ui/icons/Web";
import BorderClear from "@material-ui/icons/BorderClear";
import BorderOuter from "@material-ui/icons/BorderOuter";

function covidData() {
const API_HOST = "http://localhost:5000/topicsentiments/covid";
const [data, setData] = useState([]);

// GET request function to your Mock API
const fetchInventory = () => {
    fetch(`${API_HOST}`)
        .then(res => res.json())
        .then(json => setData(json));
}

// Calling the function on component mount
useEffect(() => {
    fetchInventory();
}, []);
const covidData = {
    totals: [ {data}
    ]
}
console.log(covidData)
return covidData
}
export default covidData;
