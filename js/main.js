var svg       = $("#statesvg"),
colorFunction = d3.scaleLinear().domain([-1, 0, 1]).range(['#FF0000', '#DDDDDD', '#00FF00']);

function tooltipHtml(n, mood,tt)
{ /* function to create html content string in tooltip div. */
	return "<h4> The average mood of a tweet about "+n+" is "+mood+"</h4> <br> <h4> Calcuated from "+tt+" tweeets."
}

rescaleAndRedraw = function()
{
	p = .9
	svg.empty();
	svg.width(svg.parent().width()*p)
	svg.height(svg.parent().width()*590/930*p)
	$.getJSON("moodData/data.json", function(moodData){states.draw(moodData, tooltipHtml);});
}

window.onresize = rescaleAndRedraw

rescaleAndRedraw()
window.setInterval(function(){$.getJSON("moodData/data.json", function(moodData){states.update(moodData, tooltipHtml);});},1000)
