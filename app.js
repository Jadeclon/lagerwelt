const express = require('express');
const bodyParser = require('body-parser')
const app = express();
const cors = require('cors');
const mysql = require('mysql');
require('dotenv').config();



const db = mysql.createPool({
      user: process.env.DB_USER,
      password: process.env.DB_PASS,
      database: process.env.DB_NAME,
      host: process.env.DB_HOST,
});

app.use(cors());
app.use(express.json());
app.use(
      express.urlencoded({
            extended: true
      })
);


app.get('/api/get', (req, res) => {
      const sql = `SELECT * FROM articles`;

      db.query(sql, (err, result) => {
            res.send(result);
      });
});


app.post('/api/insert', (req, res) => {

      const title = req.body.title;
      const description = req.body.description;
      const sql = `INSERT INTO posts (title, body) VALUES (?,?)`;

      db.query(sql, [title, description], (err, result) => {
            console.log("Sucessfully inserted!");
            console.log(result);

            if (err) console.log(err);
      });
     
});


app.delete('/api/delete/:articleId', (req, res) => {
      const articleId = req.params.articleId;
      const sql = `DELETE FROM articles WHERE articleId = ?`;

      db.query(sql, articleId, (err, result) => {
            console.log("Sucessfully deleted!");
            console.log(result);

            if (err) console.log(err);
      });
});


app.put('/api/update', (req, res) => {
      const articleId = req.body.articleId;
      const quantity = req.body.quantity;
      const sql = `UPDATE articles SET quantity = ? WHERE articleId = ?`;
      
      console.log("articleId: " + articleId);

      db.query(sql, [quantity, articleId], (err, result) => {
            console.log("Sucessfully updated!");
            if (err) console.log(err);
      });
});


app.listen(process.env.PORT || 5000, () => {
      console.log(`Running on port ${process.env.PORT}...`);
});