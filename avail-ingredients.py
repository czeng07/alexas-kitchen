# // var http = require("http"),
# //     mongojs = require("mongojs");
# //
# // var uri = "mongodb://ds117839.mlab.com:17839/avail-ingredients",
# //     db = mongojs(uri, ["avail-ingredients"]);
# //
# // var server = http.createServer(requestHandler);
# //
# // function requestHandler(request, response) {
# //
# //   response.writeHead(200, {"Content-Type": "text/html"});
# //
# //   db.avail-ingredients.find(
# //     {"color": "red"},
# //     function(err, records) {
# //
# //       if(err) {
# //         console.log("There was an error executing the database query.");
# //         response.end();
# //         return;
# //       }
# //
# //       var html = '<h2>Available ingredients</h2>',
# //         i = records.length;
# //
# //       while(i--) {
# //         html += '<p><b>Name:</b> '
# //             + records[i].name
# //             + ' <br /><b>Number of wheels:</b> '
# //             + records[i].wheels
# //             + '<br /><b>Color: </b>'
# //             + records[i].color;
# //       }
# //     response.write(html);
# //     response.end();
# //   }
# // );
# // }
# //
# // server.listen(8888);
# // console.log("Server listening on port 8888.");
# //
# // give me ten items --> return entirety of options.json




# //NEW VERSION TO USE
# //lets require/import the mongodb native drivers.
from pymongo import MongoClient
#import pymongo
import json


#import requests

#client = MongoClient('mongodb://ds117839.mlab.com:17839');
client = MongoClient("mongodb://caren:kz7j7qLF1as2ktOG@cluster0-shard-00-00-yeacn.mongodb.net:27017,cluster0-shard-00-01-yeacn.mongodb.net:27017,cluster0-shard-00-02-yeacn.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client['avail-ingredients']
#db.authenticate('caren', 'hellohellowhatup')
pantry = db['pantry']

#client.db.add_user('czeng07', 'hellohello1')

recommended = db['recommended']
currentrec= db['currentrec']
searched = db['searched']

with open('pantry.json') as data_file:
  data = json.load(data_file)
  pantry.insert(data)

with open('options.json') as data_file:
    data = json.load(data_file)
    recommended.insert(data)


#avail-ingredients.py()

# //with open('options.json')
#
#
#
#
#
#
# // var mongodb = require('mongodb');
# //
# // //We need to work with "MongoClient" interface in order to connect to a mongodb server.
# // var MongoClient = mongodb.MongoClient;
# //
# // // Connection URL. This is where your mongodb server is running.
# // var url = 'mongodb://localhost:27017/avail-ingredients';
# // //'mongodb://ds117839.mlab.com:17839/avail-ingredients',
# // //     db = mongojs(uri, ["avail-ingredients"]);
# //
# // // Use connect method to connect to the Server
# // MongoClient.connect(url, function (err, db) {
# //   if (err) {
# //     console.log('Unable to connect to the mongoDB server. Error:', err);
# //   } else {
# //     //HURRAY!! We are connected. :)
# //     console.log('Connection established to', url);
# //
# //     var collection = db.collection('avail-ingredients');
# //
# //     //Lets iterate on the result
# //     cursor.each(function (err, doc) {
# //       if (err) {
# //         console.log(err);
# //       } else {
# //         console.log('Fetched:', doc);
# //       }
# //     });
# //   }
# // });
