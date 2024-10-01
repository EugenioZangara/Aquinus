// Sparkline
var options1 = {
	series: [
		{
			data: [30, 70, 40, 65, 25, 40],
		},
	],
	chart: {
		type: "line",
		height: 35,
		width: 70,
		sparkline: {
			enabled: true,
		},
	},
	stroke: {
		curve: "smooth",
		width: 5,
	},
	colors: ["#000000"],
	tooltip: {
		fixed: {
			enabled: false,
		},
		x: {
			show: false,
		},
		y: {
			title: {
				formatter: function (seriesName) {
					return "";
				},
			},
		},
		marker: {
			show: false,
		},
	},
};

var chart8 = new ApexCharts(document.querySelector("#sparkline1"), options1);
chart8.render();
