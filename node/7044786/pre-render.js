// pre-render d3 charts at server side
var d3 = require('d3')
	, jsdom = require('jsdom')
	, fs = require('fs')
	, htmlStub = '<html><head></head><body><div id="dataviz-container"></div><script src="js/d3.v3.min.js"></script><script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script></body></html>'

	require("../XMLHttpRequest");

var width = 5000,
    height = 4000;

var data;

jsdom.env({
	features : { QuerySelector : true }
	, html : htmlStub
	, done : function(errors, window) {
	// this callback function pre-renders the dataviz inside the html document, then export result into a static file

		var el = window.document.querySelector('#dataviz-container')
			, body = window.document.querySelector('body')
			, circleId = 'a2324'  // say, this value was dynamically retrieved from some database

d3.json("test.json", function(error, json) {
  if (error) return console.warn(error);
  data = json;
  visualizeit();
});
		// generate the dataviz
		d3.select(el)
			.append('svg:svg')
				.attr('width', width)
				.attr('height', height)
				.append('circle')
					.attr('cx', 300)
					.attr('cy', 150)
					.attr('r', 30)
					.attr('fill', '#26963c')
					.attr('id', circleId) // say, this value was dynamically retrieved from some database

		// make the client-side script manipulate the circle at client side)
		var clientScript = " d3.select('#" + circleId + "').transition().delay(1000).attr('fill', '#f9af26'); "

		d3.select(body)
			.append('script')
				.html(clientScript)

		// save result in an html file, we could also keep it in memory, or export the interesting fragment into a database for later use
		var svgsrc = window.document.documentElement.innerHTML;
		fs.writeFile('index.html', svgsrc, function(err) {
			if(err) {
				console.log('error saving document', err)
			} else {
				console.log('The file was saved!')
			}
		})	
	} // end jsDom done callback
})
// no semi-column was harmed during this development