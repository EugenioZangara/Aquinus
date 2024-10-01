var options = {
	series: [15, 18, 13],
	chart: {
		height: 220,
		type: "polarArea",
	},
	labels: ["Busy", "Online", "Offline"],
	fill: {
		opacity: 1,
	},
	stroke: {
		width: 5,
		colors: ["#53a7de", "#326485", "#a9d3ef"],
	},
	colors: ["#53a7de", "#326485", "#a9d3ef"],
	yaxis: {
		show: false,
	},
	legend: {
		show: false,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val;
			},
		},
	},
	plotOptions: {
		polarArea: {
			rings: {
				strokeWidth: 0,
			},
			spokes: {
				strokeWidth: 0,
			},
		},
	},
};

var chart = new ApexCharts(document.querySelector("#agentsLiveData"), options);
chart.render();
