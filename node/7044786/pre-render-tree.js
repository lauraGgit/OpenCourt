// pre-render d3 charts at server side
var d3 = require('d3')
	, jsdom = require('jsdom')
	, fs = require('fs')
	, htmlStub = '<html><head></head><style> .node circle {fill: #fff;stroke: steelblue;stroke-width: 3px;} .node text { font: 12px sans-serif; } .link {fill: none;stroke: #ccc;stroke-width: 2px;} </style><body><div id="dataviz-container"></div><script src="js/d3.v3.min.js"></script><script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script></body></html>'

	require("../XMLHttpRequest");

var width = 5000,
    height = 4000;

var data;

jsdom.env({
	features : { QuerySelector : false }
	, html : htmlStub
	, done : function(errors, window) {

	var body = window.document.querySelector('body')
	, circleId = 'a2324';  // say, this value was dynamically retrieved from some database

	// this callback function pre-renders the dataviz inside the html document, then export result into a static file
// ************** Generate the tree diagram	 *****************
var margin = {top: 20, right: 120, bottom: 20, left: 120},
	width = 960 - margin.right - margin.left,
	height = 500 - margin.top - margin.bottom;
	
var i = 0;

var tree = d3.layout.tree()
	.size([height, width]);

var diagonal = d3.svg.diagonal()
	.projection(function(d) { return [d.y, d.x]; });

var svg = d3.select(body).append("svg")
	.attr("width", width + margin.right + margin.left)
	.attr("height", height + margin.top + margin.bottom)
  .append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// load the external data
d3.json("./treeData.json", function(error, treeData) {
	console.log(treeData);
  root = treeData[0];
  update(root);
});

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
	  links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 180; });

  // Declare the nodes…
  var node = svg.selectAll("g.node")
	  .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter the nodes.
  var nodeEnter = node.enter().append("g")
	  .attr("class", "node")
	  .attr("transform", function(d) { 
		  return "translate(" + d.y + "," + d.x + ")"; });

  nodeEnter.append("circle")
	  .attr("r", 10)
	  .style("fill", "#fff");

  nodeEnter.append("text")
	  .attr("x", function(d) { 
		  return d.children || d._children ? -13 : 13; })
	  .attr("dy", ".35em")
	  .attr("text-anchor", function(d) { 
		  return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return d.name; })
	  .style("fill-opacity", 1);

  // Declare the links…
  var link = svg.selectAll("path.link")
	  .data(links, function(d) { return d.target.id; });

  // Enter the links.
  link.enter().insert("path", "g")
	  .attr("class", "link")
	  .attr("d", diagonal);

	var svgsrc = window.document.documentElement.innerHTML;
		fs.writeFile('index.html', svgsrc, function(err) {
			if(err) {
				console.log('error saving document', err)
			} else {
				console.log('The file was saved!')
			}
		})	

}//End Update Sources



	} // end jsDom done callback
})
// no semi-column was harmed during this development