var express = require('express');
var fs = require('fs');
var dateFormat = require('dateformat');
var pyshell = require('python-shell');
var path= require('path');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Briefly' });
});

/* POST summarize */
router.post('/summarize', function(req, res, next) {
    var now = new Date();
    var name = dateFormat(new Date(), 'yyyy-mm-dd-hh-MM-ss');
    
    var options = {
        mode: 'text',
        scriptPath: path.join(__filename, '..', '..', '..', 'text-summarizer-python'),
        args: ['-f', path.join(__filename, '..', '..', 'texts', name + '.txt'), '-p', req.body.compression, '-t', 4]
    };
    if (!fs.existsSync(path.join(__filename, '..', '..', 'texts'))) {
        fs.mkdirSync(path.join(__filename, '..', '..', 'texts'));
    }
    fs.writeFile(path.join(__filename, '..', '..', 'texts', name + '.txt'), req.body.text, 'ascii', function(err) {
        if (err) {
            res.send({ error: err });
        }
        console.log("The file was saved! " + name);
        pyshell.run('text-summarizer.py', options, function (err, results) {
            if (err) {
                res.send({ error: err });
            }
          //results is an array consisting of messages collected during execution
          res.send(results);
        });
    });
});

module.exports = router;