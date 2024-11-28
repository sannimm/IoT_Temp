const express = require("express");
const app = express();
const port = process.env.PORT || 3000;
require("dotenv").config();

const cors = require("cors");
const sql = require("mssql");

const config = {
  user: process.env.user,
  password: process.env.password,
  server: process.env.host,
  database: process.env.database,
  options: {
    encrypt: true,
    enableArithAbort: true,
  },
};

sql.connect(config, (err) => {
  if (err) {
    console.error("Error connecting to the SQL server:", err);
    return;
  }
  console.log("Connected to the SQL server.");
});

app.use(express.json());
app.use(cors());

app.get("/", (req, res) => {
  res.send("Kukkuu!");
});

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  next();
});

app.get("/get_temp", (req, res) => {
  const request = new sql.Request();
  request.query("SELECT * FROM Temperature", (err, result) => {
    if (err) {
      console.error("Error executing query:", err);
      res.status(500).send("Server error");
      return;
    }
    res.json(result.recordset);
  });
});

app.post("/post_temp", (req, res) => {
  const { temp, timestamp } = req.body;
  const request = new sql.Request();
  request.input("tempValue", sql.Float, temp);
  request.input("timestampValue", sql.DateTime, timestamp);
  request.query(
    "INSERT INTO Temperature (Temp, TimeStamp) VALUES (@tempValue, @timestampValue)",
    (err, result) => {
      if (err) {
        console.error("Error executing query:", err);
        res.status(500).send("Server error");
        return;
      }
      res.json({ id: result.insertId, temp, timestamp });
    }
  );
});

app.listen(port, () => {
  console.log("Server is running on http://localhost:${port}");
});
