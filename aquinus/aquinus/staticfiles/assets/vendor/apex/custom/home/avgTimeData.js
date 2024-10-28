var options = {
	chart: {
		height: 210,
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
		width: 4,
	},
	series: [
		{
			name: "Avg. Time",
			type: "line",
			data: [0.5, 1.5, 0.5, 2, 0.5, 1.5, 0.5],
		},
	],
	grid: {
		borderColor: "#c8cfcc",
		strokeDashArray: 3,
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
	},
	xaxis: {
		categories: ["S", "M", "T", "W", "T", "F", "S"],
		labels: {
			datetimeFormatter: {
				year: "yyyy",
				month: "MMM 'yy",
				day: "dd MMM",
				hour: "HH:mm",
			},
		},
	},
	yaxis: {
		labels: {
			show: true,
		},
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val + " Hours";
			},
		},
	},
	colors: ["#e73737", "#f23c7b"],
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

var chart = new ApexCharts(document.querySelector("#avgTimeData"), options);

chart.render();
