function renderChartContainerTemplate(content, chartIndexEntry, chartNumber) {
    const chartContainerNode = content.querySelector('#chart-container');
    chartContainerNode.id = 'chart-container-' + chartNumber;

    const chartCaptionNode = content.querySelector('#chart-caption');
    chartCaptionNode.id = "chart-caption-" + chartNumber;
    chartCaptionNode.textContent = chartIndexEntry.caption;

    const chartCanvasNode = content.querySelector('#chart-canvas');
    chartCanvasNode.id = "chart-canvas-" + chartNumber;

    return content;
}

function trimChartData(forPastDays, chartDataOrigin, normalize = true) {
    if (forPastDays == 99999) {
        return chartDataOrigin;
    }

    var chartDataTrimed = [];
    dateTrimed = new Date();
    dateTrimed.setDate(dateTrimed.getDate() - forPastDays);

    for (entryOrigin of chartDataOrigin) {
        entryTrimed = {
            series : entryOrigin.series,
            points : []
        };

        var yBase = -1;
        for (pointOrigin of entryOrigin["points"]) {
            dateOrigin = new Date(pointOrigin.x);

            if (dateOrigin > dateTrimed) {

                if (normalize) {
                    if (yBase == -1) yBase = pointOrigin.y;
                    pointOrigin.y = pointOrigin.y - yBase;
                }

                entryTrimed.points.push(pointOrigin);
            }
        }
        chartDataTrimed.push(entryTrimed);
    }

    return chartDataTrimed;
}

function attachChart(context, chartData, chartType = 'line') {
    // 週次増加グラフ（棒グラフ）
    if (chartType === 'bar') {

        const labels = chartData[0].points.map(point => {
            const date = new Date(point.x);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric'
            });
        });

        const datasets = chartData.map(entry => ({
            label: entry.series,
            data: entry.points.map(point => point.y),
            fill: false
        }));

        new Chart(context, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkip: false,
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                legend: {
                    position: 'right'
                },
                plugins: {
                    colorschemes: {
                        scheme: 'brewer.Paired12'
                    }
                }
            }
        });

        return;
    }

    // 既存の折れ線グラフ
    var datasets = [];

    for (entry of chartData) {
        datasets.push({
            label: entry.series,
            data: entry.points,
            fill: false
        });
    }

    new Chart(context, {
        type: chartType,
        data: {
            datasets: datasets
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                position: 'right'
            },
            plugins: {
                colorschemes: {
                    scheme: 'brewer.Paired12'
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const saveState = sessionStorage.getItem('forThePastDates');
    const forThePastDates = saveState ? parseInt(saveState, 10) : 99999;

    const parentNode = document.querySelector('#chart-plain');
    const templateContent = document.querySelector('#chart-container-template').content;

    fetch('assets/chart-index.json')
        .then(response => response.json())
        .then(chartIndex => {
            for (let i = 0; i < chartIndex.length; i++) {
                const content = document.importNode(templateContent, true);
                const renderedContent = renderChartContainerTemplate(content, chartIndex[i], i);
                parentNode.appendChild(renderedContent);

                fetch(chartIndex[i].data_file)
                    .then(response => response.json())
                    .then(chartDataOrigin => {

                        return trimChartData(
                            forThePastDates,
                            chartDataOrigin,
                            chartIndex[i].trim !== false
                        );
                    })
                    .then(chartData => {
        
                        const context = document.getElementById("chart-canvas-" + i);
                        attachChart(
                            context,
                            chartData,
                            chartIndex[i].chart_type || 'line'
                        )
                    });
            }
        });
});

var forThePast030Dates = document.getElementById('forThePast030Dates');
forThePast030Dates.addEventListener('click', () => {
    sessionStorage.setItem('forThePastDates', '30');
    location.reload();
});

var forThePast060Dates = document.getElementById('forThePast060Dates');
forThePast060Dates.addEventListener('click', () => {
    sessionStorage.setItem('forThePastDates', '60');
    location.reload();
});

var forThePast180Dates = document.getElementById('forThePast180Dates');
forThePast180Dates.addEventListener('click', () => {
    sessionStorage.setItem('forThePastDates', '180');
    location.reload();
});

var forThePastAllDates = document.getElementById('forThePastAllDates');
forThePastAllDates.addEventListener('click', () => {
    sessionStorage.removeItem('forThePastDates');
    location.reload();
});
