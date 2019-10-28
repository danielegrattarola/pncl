let charts = [];

function renderGrid(plots, grid) {
    // Create charts
    for (let idx = 0; idx < plots.length; idx++) {
        let ij = idxToCoords(idx, grid);
        let i = ij[0];
        let j = ij[1];
        let ctx = document.getElementById(`canvas-${i}-${j}`).getContext('2d');
        let chart = new Chart(ctx, plots[idx]);
        charts.push(chart);
    }
}


function createCanvasGrid(grid, colHeight) {
    for (let i = 0; i < grid.length; i++) {
        createRow(i, grid[i], colHeight + "px");
    }
}


function createRow(rowIdx, cols, colHeight) {
    // Add Bootstrap row
    let row = document.createElement("div");
    row.className = 'row';
    row.id = `row-${rowIdx}`;
    document.getElementById('wrapper').appendChild(row);

    // Create columns
    for (let col = 0; col < cols; col++) {
        // Create canvas container
        let div = document.createElement("div");
        div.className = 'plot col-sm';
        div.id = `plot-${rowIdx}-${col}`;

        // Add canvas
        div.innerHTML = `
            <canvas id="canvas-${rowIdx}-${col}" style="height: ${colHeight};"></canvas>
        `;
        row.appendChild(div);

        // Save images on click
        $(`#canvas-${rowIdx}-${col}`).click(function() {
            let link = document.createElement("a");
            link.setAttribute('download', $(this).attr('id') + '.png');
            link.setAttribute('href', $(this)[0].toDataURL("image/png").replace("image/png", "image/octet-stream"));
            link.click();
        });
    }
}


/*  */
function clearGrid() {
    // Destroy all Chart objects and clear list
    for (let chartIdx = 0; chartIdx < charts.length; chartIdx++) {
        charts[chartIdx].destroy();
    }
    charts.length = 0;

    // Remove all divs
    let divs = document.getElementsByClassName('plot');
    while (divs[0]) {
        divs[0].parentElement.parentElement.removeChild(divs[0].parentElement);
    }
}


// Helpers
function idxToCoords(idx, grid) {
    let counter = 0;
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i]; j++) {
            if (counter === idx) {
                return [i, j];
            } else {
                counter += 1;
            }
        }
    }
}


function log(arg) {
    console.log(arg);
}

/*******************************************************************************
* MAIN
*******************************************************************************/
Chart.plugins.register({
  beforeDraw: function(chartInstance) {
    var ctx = chartInstance.chart.ctx;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
  }
});

$.ajax({
    type: 'GET',
    url: '/config',
    async: false,
    success: function(data) {
        let eventJSON = JSON.parse(data);
        clearGrid();
        const grid = eventJSON.grid;
        const colHeight = eventJSON.height;
        createCanvasGrid(grid, colHeight);
        renderGrid(eventJSON.plots, grid);
    }
});

let source = new EventSource("/event");
source.onmessage = function(event) {
    let idx;
    let eventJSON = JSON.parse(event.data);
    if (eventJSON.type === 'new_grid') {
        log(eventJSON.type);
        clearGrid();
        const grid = eventJSON.data.grid;
        const colHeight = eventJSON.data.height;
        createCanvasGrid(grid, colHeight);
        renderGrid(eventJSON.data.plots, grid);
    } else if (eventJSON.type === 'refresh') {
        log(eventJSON.type);
        idx = eventJSON.idx;
        Object.assign(charts[idx].config, eventJSON.data);
        Object.assign(charts[idx].options, eventJSON.data.options);
        charts[idx].update();
    } else if (eventJSON.type === 'push') {
        log(eventJSON.type);
        idx = eventJSON.idx;
        if (charts[idx].data.labels != null) {
            charts[idx].data.labels.push(eventJSON.data.label);
        }
        for (let i = 0; i < eventJSON.data.datasets.length; i++) {
             for (let key in eventJSON.data.datasets[i]){
                charts[idx].data.datasets[i][key].push(eventJSON.data.datasets[i][key]);
            }
        }
        charts[idx].update();
    }
    else {
        log('No events');
    }
};
