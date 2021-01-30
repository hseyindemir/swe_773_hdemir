import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Paper from "@material-ui/core/Paper";
import { PieChart, Pie, Tooltip, ResponsiveContainer } from "recharts";
import GlobalStyles from "../../styles.scss";
import { orange } from "@material-ui/core/colors";
import { TextsmsTwoTone } from "@material-ui/icons";

const BrowserUsage = props => {
  const styles = {
    paper: {
      minHeight: 344,
      padding: 0
    },
    legend: {
      paddingTop: 20
    },
    pieChartDiv: {
      height: 290,
      textAlign: "center"
    },
    header: {
      fontSize: 24,
      fontWeight: 300,
      backgroundColor: orange[600],
      color: "white",
      lineHeight: "48px",
      paddingLeft: "10px"
    }
  };

  
  function test222() {
    const test= [
      { name: "Chrome", value: 800 },
      { name: "yesss", value: 300 },
      { name: "huss", value: 300 }
    ]
    const API_HOST = "http://localhost:5000/mostsimilars/covid";
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
    return data
  }
  let title = test222();

  return (
    <Paper style={styles.paper}>
      <div style={{ ...GlobalStyles.title, ...styles.header }}>
        Browser Usage
      </div>

      <div style={GlobalStyles.clear} />

      <div style={styles.pieChartDiv}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              dataKey="count"
              nameKey="keyword"
              colorKey="color"
              innerRadius={60}
              outerRadius={100}
              data= {title}
              fill="#8884d8"
              label
            />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </Paper>
  );
};

BrowserUsage.propTypes = {
  data: PropTypes.array
};

export default BrowserUsage;
