// pre-render d3 charts at server side
var d3 = require('d3')
	, jsdom = require('jsdom')
	, fs = require('fs')
	, htmlStub = '<html><head></head><style>  body {    font-family: sans-serif;  }    .node {    /*stroke: #fff;    stroke-width: 1.5px;    stroke-opacity: .4;*/    fill-opacity: .6;  }    .link {    stroke: #999;    stroke-opacity: .2;  }    /*.dark {    fill-opacity: 1;  }*/    .d3-tip {    line-height: 1;    /*font-weight: bold;*/    padding: 12px;    background: rgba(0, 0, 0, 0.8);    color: #fff;    border-radius: 2px;  }    /* Creates a small triangle extender for the tooltip */  .d3-tip:after {    box-sizing: border-box;    display: inline;    font-size: 10px;    width: 100%;    line-height: 1;    color: rgba(0, 0, 0, 0.8);    content: "\25BC";    position: absolute;    text-align: center;  }    /* Style northward tooltips differently */  .d3-tip.n:after {    margin: -1px 0 0 0;    top: 100%;    left: 0;  }    </style><script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script></body></html>'

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
	width = 5000 - margin.right - margin.left,
	height = 4000 - margin.top - margin.bottom;
	
var i = 0;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-10)
    .linkDistance(5)
    .size([width, height]);

var svg = d3.select(body).append("svg")
    .attr("width", width)
    .attr("height", height);

var caseify = function(cNum){
  cNum = cNum.slice(1,-1);
  cArr = cNum.split(",");
  return cArr[0] + " U.S. "+ cArr[1];
};
// load the external data
d3.json("graph1-575-0615.json", function(error, caseData) {
	//console.log(caseData);
  update(caseData);
});

function update(graph) {

force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append("circle")
      .attr("class", "node")
      .attr("r", 3)
      .attr("data-vol", function(d){d.vol})
      .attr("data-year", function(d){d.year})
      .attr("data-name", function(d){d.name})
      .attr("data-id", function(d){d.id})
      .style("fill", function(d) { return color(d.year); });
      //.call(force.drag);

  // var tip = d3.tip()
  // .attr('class', 'd3-tip')
  // .offset([-10, 0])
  // .html(function(d) {
  //   return d.name +"<br />Volume: " + d.vol +"<br /> Year: " +d.year+"<br/>" + caseify(d.id);
  // })

  // node.append("title")
  //     .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

  //svg.call(tip);  

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
       // .on('mouseover', tip.show)
       // .on('mouseout', tip.hide);
  });

  //Write file after animation finishes
  force.on("end", function() {
  		var svgsrc = window.document.documentElement.innerHTML;
		fs.writeFile('index.html', svgsrc, function(err) {
			if(err) {
				console.log('error saving document', err)
			} else {
				console.log('The file was saved!')
			}
		});
  });
	

}//End Update Sources



	} // end jsDom done callback
})
// no semi-column was harmed during this development