import * as d3 from 'd3';
import _ from 'underscore';

d3.json('static/dummy.json', draw);

function draw(err, data) {
  if (err) {
    console.log(error);
  }
  else {
    const fontScale = d3.scaleLinear().range([1, 3]).domain(d3.extent(_.pluck(data, 'score')));
    const fontMap = d => fontScale(d.score) + 'em';
    const rows = d3.select('tbody').selectAll('tr').data(data, d => d.name);

    rows.enter()
      .append('tr')
      .style('font-size', fontMap) 
      .each(function (d) {
        const row = d3.select(this);
        row.append('td').text(d => d.name);
        row.append('td').classed('score', true).text(d.score);
      })
      ;

    rows
      .style('font-size', fontMap)
      .each(function (d) {
        d3.select(this).select('td.score').text(d.score);
      })
      ;

    rows.sort((a, b) => (b.score - a.score));

    window.setTimeout(draw, 2000, null, randomize(data));
  }
}

function randomize(data) {
  return _.map(data, d => {
    d.score += Math.round(Math.random() * 10);
    return d;
  });
}
