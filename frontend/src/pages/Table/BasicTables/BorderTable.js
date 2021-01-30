import React, { useEffect, useState } from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import { withStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Divider from "@material-ui/core/Divider";
import Typography from "@material-ui/core/Typography";
import Data from "../../../data";
import covidData from "../../../apiData"
import styles from "./tableColumnStyle";

const borderedTableStyle = theme => ({
  table: {
    border: "1px solid rgba(0, 0, 0, 0.12)"
  }
});

const API_HOST = "http://35.238.161.243:5000/topicsentiments/covid";
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
      <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          test
        </Typography>
        <Divider />
        <Table>
          <TableHead>
            <TableRow>
              <TableCell style={styles.columns.id}>ID</TableCell>
              <TableCell style={styles.columns.name}>Name</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(item => (
              <TableRow key={item.positivity}>
                <TableCell style={styles.columns.id}>{item.comment}</TableCell>
                <TableCell style={styles.columns.category}>
                  {item.positivity}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}


export default App;
