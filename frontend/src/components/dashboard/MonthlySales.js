import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Paper from "@material-ui/core/Paper";
import { BarChart, Bar, ResponsiveContainer, XAxis } from "recharts";
import GlobalStyles from "../../styles.scss";

import { withStyles } from "@material-ui/core/styles";

const MonthlySales = ({ data, theme }) => {
  const styles = {
    paper: {
      backgroundColor: theme.palette.secondary[600],
      height: 150
    },
    div: {
      marginLeft: "auto",
      marginRight: "auto",
      width: "95%",
      height: 85
    },
    header: {
      color: "white",
      backgroundColor: theme.palette.secondary[600],
      padding: 10,
      fontSize: 24
    }
  };
  
  function getSimilarKeywords() {
    const API_HOST = "http://localhost:5000/mostusedwordsinsubreddits/covid";
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
  let similarKeywordData = getSimilarKeywords();

  return (
    <Paper style={styles.paper}>
      <div style={{ ...GlobalStyles.title, ...styles.header }}>
        Most used words regarding covid results
      </div>
      <div style={styles.div}>
        <ResponsiveContainer>
          <BarChart data={similarKeywordData}>
            <Bar dataKey="count" fill={theme.palette.primary[200]} />
            <XAxis
              dataKey="keyword"
              stroke="none"
              tick={{ fill: theme.palette.common.white }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Paper>
  );
};

MonthlySales.propTypes = {
  data: PropTypes.array,
  theme: PropTypes.object
};

export default withStyles(null, { withTheme: true })(MonthlySales);