import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Paper from "@material-ui/core/Paper";
import GlobalStyles from "../../styles.scss";
import { BarChart, Bar, ResponsiveContainer, XAxis } from "recharts";
import { withStyles } from "@material-ui/core/styles";

const API_HOST = "http://35.238.161.243:5000/mostusedwordsinsubreddits/covid";

function App() {


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

    return (
        <Paper>
        <div>New Orders</div>
        <div>
        <ResponsiveContainer>
       
          <BarChart data={data}>
            <Bar dataKey="uv" />
            <XAxis
              dataKey="name"
              stroke="none"
            />
         
          </BarChart>
        </ResponsiveContainer>
        </div>
      </Paper>
 
  );
}


export default App;
