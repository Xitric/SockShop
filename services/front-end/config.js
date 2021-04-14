(function (){
  'use strict';

  var util         = require("util"),
      session      = require("express-session"),
      redis        = require("redis"),
      RedisStore   = require('connect-redis')(session)

  var domain = "";
  if (process.env.DOMAIN) {
      domain = "." + process.env.DOMAIN;
      console.log("Environment variable setting domain to:", domain);
  }

  process.argv.forEach(function (val, index, array) {
    var arg = val.split("=");
    if (arg.length > 1) {
      if (arg[0] == "--domain") {
        domain = "." + arg[1];
        console.log("System parameter setting domain to:", domain);
      }
    }
  });

  const client = redis.createClient({
      host: util.format("session-db%s", domain)
  });
  client.on('error', err => {
    console.log('Redis error ' + err);
  });

  module.exports = {
    session: {
      name: 'md.sid',
      secret: 'sooper secret',
      resave: false,
      saveUninitialized: true
    },
    
    session_redis: {
      store: new RedisStore({client: client}),
      name: 'md.sid',
      secret: 'sooper secret',
      resave: false,
      saveUninitialized: true
    }
  };
}());
