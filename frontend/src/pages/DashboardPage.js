import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { cyan, pink, purple, orange } from "@material-ui/core/colors";
import Assessment from "@material-ui/icons/Assessment";
import Face from "@material-ui/icons/Face";
import ThumbUp from "@material-ui/icons/ThumbUp";
import ShoppingCart from "@material-ui/icons/ShoppingCart";
import InfoBox from "../components/dashboard/InfoBox";
import NewOrders from "../components/dashboard/NewOrders";
import MonthlySales from "../components/dashboard/MonthlySales";
import WordCountDist from "../components/dashboard/WordCountDist";
import BrowserUsage from "../components/dashboard/BrowserUsage";
import RecentlyProducts from "../components/dashboard/RecentlyProducts";
import globalStyles from "../styles";
import Grid from "@material-ui/core/Grid";
import Data from "../data";
import { BarChart } from "recharts";
import SimpleTable from "../pages/Table/BasicTables/SimpleTable"
import StripedTable from "../pages/Table/BasicTables/StripedTable";

const API_HOST = "http://localhost:5000/totalsinredditfiltered/covid";

function DashboardPage() {


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
    <div>
      <h3 style={globalStyles.navigation}>Application / Dashboard</h3>


      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Link to="/table/data" className="button">
            <InfoBox Icon={Assessment} color={pink[600]} title="Total Comment for Covid" value={data.totalComment} />
          </Link>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox Icon={Assessment} color={cyan[600]} title="Total Reddits for Covid" value={data.totalSubreddit} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox Icon={Assessment} color={purple[600]} title="Average Positivity Score for Topics" value={data.averageScore} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox Icon={Assessment} color={orange[600]} title="Average Positivity Score for Comments" value={data.averageScoreComment} />
        </Grid>
      </Grid>

      <Grid container spacing={10} xl={24} lg={12}>
        <Grid item xs={24} sm={12}>
          <MonthlySales/>
        </Grid>
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <SimpleTable />
        </Grid>
        <Grid item xs={12} sm={6}>
          <StripedTable />
        </Grid>
      </Grid>
     
    </div>
  );
};

export default DashboardPage;
