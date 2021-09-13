const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');
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

app.use(cors({
      origin: ["https://lagerwelt3000.netlify.app"],
      // origin: ["http://localhost:3000"],
      methods: ["GET", "POST", "PUT"],
      credentials: true
}));
app.use(express.json());
app.use(
      express.urlencoded({
            extended: true
      })
);
app.use(cookieParser());
// app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
            key: "userId",
            secret: "important",
            resave: false,
            saveUninitialized: false,
            cookie: {
                  expires: 3600000,
            },
      })
);


app.get('/api/get', (req, res) => {
      const sql = `SELECT * FROM artikel`;

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


app.post('/login', (req, res) => {
      const username = req.body.username;
      const password = req.body.password;

      db.query("SELECT * FROM benutzer WHERE user = ?",
            [username], (err, result) => {

                  if(err) { console.log }

                  if(result.length > 0) {
                        if(password === result[0].password) {
                              req.session.user = result;
                              console.log(req.session.user);
                              res.send("Logged in successfully!");
                        } else {
                              res.send("Wrong username/password combination!");
                        }
                  } else {
                        res.send("Wrong username/password combination!");
                  }
            }
      );
});


app.get("/login", (req, res) => {
      if(req.session.user) {
            res.send({ loggedIn: true, user: req.session.user });
      } else {
            res.send({ loggedIn: false });
      }
});


app.delete('/api/delete/:articleId', (req, res) => {
      const articleId = req.params.articleId;
      const sql = `DELETE FROM artikel WHERE artikel_Id = ?`;

      db.query(sql, articleId, (err, result) => {
            console.log("Sucessfully deleted!");
            console.log(result);

            if (err) console.log(err);
      });
});


app.put('/api/updateQuantity', async (req, res) => {
      const articleId = req.body.articleId;
      const quantity = req.body.quantity;
      const sql = `UPDATE articles SET Anzahl = ? WHERE artikel_Id = ?`;
      
      console.log("articleId: " + articleId);

      db.query(sql, [quantity, articleId], (err, result) => {
            console.log("Sucessfully updated!");
            if (err) console.log(err);
      });
});

app.put('/api/update', async (req, res) => {
      const article = req.body.article;
      const sql = `UPDATE articles SET articleNumber = ?, storagePlace = ?, manufacturer = ? WHERE articleId = ?`;
      
      console.log("Updating " + article.articleNumber);

      db.query(sql, [article.articleNumber, article.storagePlace, article.manufacturer, article.articleId], (err, result) => {
            if (err) console.log(err);

            // res.send("Sucessfully updated " + article.articleNumber);
      });
});


app.listen(process.env.PORT || 5000, () => {
      console.log(`Running on port ${process.env.PORT}...`);
});