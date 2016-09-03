var runs =0;
var colorFunction = d3.scaleLinear()
    .domain([-1, 0, 1])
    .range(['#FF0000', '#EEEEEE', '#00FF00']);


var sampleData
function tooltipHtml(n, mood)
{ /* function to create html content string in tooltip div. */
	return "<h4> The average mood of a tweet about "+n+" is "+mood+"</h4>"
}
window.setInterval(
	function()
		{
		var moodData 
		$.getJSON("moodData/data.json", 
			function(json) 
				{
				moodData = json;
				statesName = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}

				

				sampleData ={}; /* Sample random data. */ 
				["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA",
				"ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH", 
				"MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT", 
				"CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN", 
				"WI", "MO", "AR", "OK", "KS", "LA", "VA"]
				.forEach
				(
					function(d)
					{ 
						var mood      = moodData[statesName[d]]
						sampleData[d] = 
										{
											mood:mood,
											color:colorFunction(mood)
										}; 
					}
				);

				if (runs==0)
				{
					
					states.draw(sampleData, tooltipHtml);
				}
				if (runs>1)
				{
					states.update(sampleData, tooltipHtml);
				};
				runs = runs+1
				
				d3.select(self.frameElement).style("height", "60px"); 
				}
			);
		}
,10)
