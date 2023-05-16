'use strict';
setTimeout(async function() {
    // ESP 1
    // data iot
    const response = await fetch('/data');
    const datas = await response.json();
    
    
    // filter datas
    // times in format hour : minute
    const timesData = datas.map(data => {
        const { hour, minute } = data;
        const clockFormat = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        return clockFormat;        
    });
    // console.log('times:',timesData);

    // dates
    const dateTimeFormats = datas.map(data => {
        const { day, hour, minute, month } = data;
        const year = new Date().getFullYear();
        const dateTimeFormat = `${day.toString().padStart(2, '0')}-${month}-${year} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        return dateTimeFormat;
    });
    // console.log('dates:',dateTimeFormats);
    // values
    const values = datas.map(data => {
        const { value } = data;
        return value;
    });
    // console.log('val:',values);
    
    // ESP 1
    // data iot
    const response2 = await fetch('/datadua');
    const datas2 = await response2.json();
    
    
    // filter datas
    // times in format hour : minute
    const timesData2 = datas2.map(data => {
        const { hour, minute } = data;
        const clockFormat = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        return clockFormat;        
    });
    // console.log('times:',timesData);

    // dates
    const dateTimeFormats2 = datas2.map(data => {
        const { day, hour, minute, month } = data;
        const year = new Date().getFullYear();
        const dateTimeFormat = `${day.toString().padStart(2, '0')}-${month}-${year} ${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
        return dateTimeFormat;
    });
    // console.log('dates:',dateTimeFormats);
    // values
    const values2 = datas2.map(data => {
        const { value } = data;
        return value;
    });
    // console.log('val:',values);
    
    // charts
    (function () {
        var options = {
            chart: {
                height: 300,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false,
                width: 2,
            },
            stroke: {
                curve: 'straight',
            },
            colors: ["#4099ff"],
            fill: {
                type: "gradient",
                gradient: {
                    shade: 'light'
                },
            },
            series: [{
                name: "Analog value",
                data: values
            }],
            title: {
                text: 'Gases Concentration Trends by times',
                align: 'left'
            },
            grid: {
                row: {
                    colors: ['#f3f6ff', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            },
            xaxis: {
                categories: dateTimeFormats,
            }
        }
        var chart = new ApexCharts(
            document.querySelector("#line-chart-1"),
            options
        );
        chart.render();
    })();
    (function () {
        var options = {
            chart: {
                height: 300,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false,
                width: 2,
            },
            stroke: {
                curve: 'straight',
            },
            colors: ["#4099ff"],
            fill: {
                type: "gradient",
                gradient: {
                    shade: 'light'
                },
            },
            series: [{
                name: "Analog value",
                data: values2
            }],
            title: {
                text: 'Gases Concentration Trends by times',
                align: 'left'
            },
            grid: {
                row: {
                    colors: ['#f3f6ff', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            },
            xaxis: {
                categories: dateTimeFormats2,
            }
        }
        var chart = new ApexCharts(
            document.querySelector("#line-chart-2"),
            options
        );
        chart.render();
    })();
}, 700);