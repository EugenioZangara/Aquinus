var options = {
	chart: {
		height: 285,
		type: "line",
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "straight",
		width: 3,
		colors: ["#53a7de", "#a7a8a6", "#d2d8e3"],
	},
	series: [
		{
			name: "New",
			data: [10, 40, 15, 40, 20, 35, 20],
		},
		{
			name: "Closed",
			data: [2, 21, 4, 20, 6, 22, 39],
		},
	],
	grid: {
		borderColor: "#c8cfcc",
		strokeDashArray: 5,
		xaxis: {
			lines: {
				show: true,
			},
		},
		yaxis: {
			lines: {
				show: false,
			},
		},
		padding: {
			top: 0,
			right: 0,
			bottom: 10,
			left: 0,
		},
	},
	xaxis: {
		categories: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
	},
	yaxis: {
		labels: {
			show: false,
		},
	},
	colors: ["#53a7de", "#a7a8a6", "#d2d8e3"],
	markers: {
		size: 0,
		opacity: 0.3,
		colors: ["#53a7de", "#a7a8a6", "#d2d8e3"],
		strokeColor: "#ffffff",
		strokeWidth: 2,
		hover: {
			size: 7,
		},
	},
	fill: {
		type: "gradient",
		gradient: {
			shade: "dark",
			type: "horizontal",
			shadeIntensity: 0.1,
			gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
			inverseColors: true,
			opacityFrom: 1,
			opacityTo: 1,
			stops: [0, 100],
			colorStops: [],
		},
	},
};

var chart = new ApexCharts(document.querySelector("#newClosedGraph"), options);

chart.render();
