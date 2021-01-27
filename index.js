const express = require("express");
const app = express();
const path = require("path");
const mysql = require("mysql");

app.use("/client/public", express.static(path.join(__dirname, "client/public")));
app.use("/client/src", express.static(path.join(__dirname, "client/src")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "client/public", "index.html"));
});

app.get("/api", function (req, res) {
  const connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "", // secure password entry?
    database: "52_week_high_freq",
  });
  connection.connect((err) => {
    connection.query("SELECT * FROM freq_stocks;", (err, rows) => {
      if (err) console.log(err);
      console.log("connection successful");
      res.json(rows);
    });
  });
});
app.listen(5000, function () {
  console.log("server is listening at port 5000...");
});
