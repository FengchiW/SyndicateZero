const express = require('express');
const router = express.Router();

router.get('/', (req, res, next) => {
  res.render('index', {title: "Syndicate Zero"})
});


router.get('/play', (req, res, next) => {
  res.render('game', {title: "Syndicate Zero"})
});

module.exports = router;
