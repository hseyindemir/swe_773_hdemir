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
import TempBar from "../components/dashboard/TempBar";
import WordCountDist from "../components/dashboard/WordCountDist";
import BrowserUsage from "../components/dashboard/BrowserUsage";
import RecentlyProducts from "../components/dashboard/RecentlyProducts";
import globalStyles from "../styles";
import Grid from "@material-ui/core/Grid";
import Data from "../data";
import SimpleTable from "../pages/Table/BasicTables/SimpleTable";
import StripedTable from "../pages/Table/BasicTables/StripedTable";
import { Button, FormControl, TextField } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Divider from "@material-ui/core/Divider";
import Typography from "@material-ui/core/Typography";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import styles from "../pages/Table/BasicTables/tableColumnStyle";
import { withStyles } from "@material-ui/core/styles";
import { BarChart, Bar, ResponsiveContainer, XAxis } from "recharts";
import Paper from "@material-ui/core/Paper";
import GlobalStyles from "../styles.scss";

const API_HOST = "http://35.238.161.243:5000";


function KeywordPage() {
  const [data, setData] = useState([]);
  const [keyword, setKeyword] = useState([]);
  const [dataByKeyword, setDataByKeyword] = useState([]);

  // GET request function to your Mock API
  const fetchInventory = () => {
    fetch(`${API_HOST}/totalsinredditfiltered/covid`)
      .then((res) => res.json())
      .then((json) => setData(json));
  };

  const fetchKeywordData = () => {
    const settings = {
      method: "get",
      headers: { "Content-Type": "application/json" },
     
    };

    console.log(JSON.stringify("fetchKeywordData" + JSON.stringify(settings)));
    fetch(`${API_HOST}/totalsinredditv2/${keyword}`, settings)
      .then((res) => res.json())
      .then((json) => setData(json));
  };

  const handleSubmit = () => fetchKeywordData();


  // Calling the function on component mount
  useEffect(() => {
    fetchInventory();
    fetchKeywordData("covid");
  }, []);
  

  return (
    <div>
      <h2 style={{ color: "black" }}>Search for a keyword here:</h2>
      <div>
        <FormControl>
          <TextField
            style={{}}
            placeholder="Search"
            size="small"
            variant="filled"
            onChange={(e) => {
              setKeyword(e.target.value);
            }}
          >
            Keyword:
          </TextField>
          <Button
            style={{
              backgroundColor: "#0b60a3",
              color: "white",
              left: "110%",
              bottom: "45px",
            }}
            size="large"
            onClick={handleSubmit}
          >
            Search
          </Button>
        </FormControl>
      </div>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Link to="/table/data" className="button">
            <InfoBox
              Icon={Assessment}
              color={pink[600]}
              title="Total Comments"
              value={data.totalComment}
            />
          </Link>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox
            Icon={Assessment}
            color={cyan[600]}
            title="Total Reddits"
            value={data.totalSubreddit}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox
            Icon={Assessment}
            color={purple[600]}
            title="Average Positivity Score for Topics"
            value={data.averageScore}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <InfoBox
            Icon={Assessment}
            color={orange[600]}
            title="Average Positivity Score for Comments"
            value={data.averageScoreComment}
          />
        </Grid>
      </Grid>

      <Grid container spacing={10} xl={24} lg={12}>
      <Grid item xs={24} sm={12}>
          <TempBar data={data && data.keywordList && data.keywordList ? data.keywordList : {}} />
        </Grid>
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
        <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          The Most Populars Topics in {keyword}
        </Typography>
        <Divider />
        <Table>
          <TableHead>
            <TableRow>
              <TableCell style={styles.columns.id}>Topic Score</TableCell>
              <TableCell style={styles.columns.name}>Topic Title</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
          {data && data.highReddits && data.highReddits.map(item => (
              <TableRow key={item.topicScore}>
                <TableCell style={styles.columns.id}>{item.topicScore}</TableCell>
                <TableCell style={styles.columns.category}>
                  {item.topicTitle}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
        <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          The Most Populars Topics in about {keyword}
        </Typography>
        <Divider />
        <Table>
          <TableHead>
            <TableRow>
              <TableCell style={styles.columns.id}>Topic Score</TableCell>
              <TableCell style={styles.columns.name}>Topic Title</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
          {data && data.upvoteReddits && data.upvoteReddits.map(item => (
              <TableRow key={item.upvoteRatio}>
                <TableCell style={styles.columns.id}>{item.upvoteRatio}</TableCell>
                <TableCell style={styles.columns.category}>
                  {item.topicTitle}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
        </Grid>

      </Grid>
    </div>
  );
}

export default KeywordPage;
