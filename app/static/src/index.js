import * as d3 from 'd3';
import _ from 'underscore';

function roundPoints(d) {
  return Math.round(d.points * 1000)/1000;
}

function update() {
  d3.json('get_scoreboard', draw);
}

update();

function draw(err, data) {
  if (err) {
    update();
  }
  else {
    data = _.sortBy(data, d => -d.points);

    const fontScale = d3.scaleLinear().range([1, 3]).domain(d3.extent(_.pluck(data, 'points')));
    const fontMap = d => fontScale(d.points) + 'em';
    const rows = d3.select('tbody').selectAll('tr').data(data, d => d.name);

    rows.enter()
      .append('tr')
      .style('font-size', fontMap) 
      .each(function (d) {
        const row = d3.select(this);
        row.append('td').text(d => d.name);
        row.append('td').classed('points', true).text(roundPoints);
      })
      ;

    rows
      .style('font-size', fontMap)
      .each(function (d) {
        d3.select(this).select('td.points').text(roundPoints);
      })
      ;

    rows.sort((a, b) => (b.points - a.points));

    rows.exit().remove();

    window.setTimeout(update, 5000);
  }
}
