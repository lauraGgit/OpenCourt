  var forever = require('forever-monitor');

  var child = new (forever.Monitor)('7044786/pre-render-force-em.js', {
    max: 3,
    silent: false,
    outFile: 'mylog.log'
  });

  child.on('exit', function () {
    console.log('your-filename.js has exited after 3 restarts');
  });

  child.on('start', function () {
    console.log('7044786/pre-render-force-em.js has started');
  });

  child.start();