var http = require("http"),
    mongojs = require("mongojs");

var uri = "mongodb://ds117839.mlab.com:17839/avail-ingredients",
    db = mongojs(uri, ["avail-ingredients"]);



var server = http.createServer(requestHandler);

function requestHandler(request, response) {

  response.writeHead(200, {"Content-Type": "text/html"});

  db.avail-ingredients.find(
    {"color": "red"},
    function(err, records) {

      if(err) {
        console.log("There was an error executing the database query.");
        response.end();
        return;
      }

      var html = '<h2>Available ingredients</h2>',
        i = records.length;

      while(i--) {
        html += '<p><b>Name:</b> '
            + records[i].name
            + ' <br /><b>Number of wheels:</b> '
            + records[i].wheels
            + '<br /><b>Color: </b>'
            + records[i].color;
      }
    response.write(html);
    response.end();
  }
);
}

server.listen(8888);
console.log("Server listening on port 8888.");





//NEW VERSION TO USE
// //lets require/import the mongodb native drivers.
// var mongodb = require('mongodb');
//
// //We need to work with "MongoClient" interface in order to connect to a mongodb server.
// var MongoClient = mongodb.MongoClient;
//
// // Connection URL. This is where your mongodb server is running.
// var url = 'mongodb://localhost:27017/avail-ingredients';
// //'mongodb://ds117839.mlab.com:17839/avail-ingredients',
// //     db = mongojs(uri, ["avail-ingredients"]);
//
// // Use connect method to connect to the Server
// MongoClient.connect(url, function (err, db) {
//   if (err) {
//     console.log('Unable to connect to the mongoDB server. Error:', err);
//   } else {
//     //HURRAY!! We are connected. :)
//     console.log('Connection established to', url);
//
//     // Get the documents collection
//     var collection = db.collection('users');
//
//     //We have a cursor now with our find criteria
//     var cursor = collection.find({name: 'modulus user'});
//
//     //We need to sort by age descending
//     cursor.sort({age: -1});
//
//     //Limit to max 10 records
//     cursor.limit(10);
//
//     //Skip specified records. 0 for skipping 0 records.
//     cursor.skip(0);
//
//     //Lets iterate on the result
//     cursor.each(function (err, doc) {
//       if (err) {
//         console.log(err);
//       } else {
//         console.log('Fetched:', doc);
//       }
//     });
//   }
// });
