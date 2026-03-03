<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { getMembersFromYear, getYearsServed } from './../shared/getmembers.js';

  let container;

  onMount(async () => {
    const width = 640;
    const height = 400;
    const marginTop = 20;
    const marginRight = 20;
    const marginBottom = 30;
    const marginLeft = 60;

    const year = 2024;
    const chamber = 'Both';

    const data = await d3.json('/data/members.json');
    const filteredData = getMembersFromYear(chamber, year, data);
    const yearsServed = getYearsServed(year, filteredData);

    const bin = d3.bin().domain([25, 110]).thresholds([31, 41, 51, 61, 71, 81]).value(d => d[1]);
    const bins = bin(yearsServed);

    const yearsServedAverages = [];
    bins.forEach(bin => {
      let totalYearsHouse = 0;
      let totalYearsSenate = 0;
      bin.forEach(member => {
        totalYearsHouse += member[2];
        totalYearsSenate += member[3];
      });
      const averageYearsHouse = bin.length === 0 ? 0 : Math.round(totalYearsHouse / bin.length);
      const averageYearsSenate = bin.length === 0 ? 0 : Math.round(totalYearsSenate / bin.length);
      yearsServedAverages.push([averageYearsHouse, averageYearsSenate]);
    });

    const xLabels = bins.map((d, i) => {
      if (i === 0) return '<= 31';
      else if (i === bins.length - 1) return '> 80';
      else return `${d.x0}-${d.x1 - 1}`;
    });

    const x = d3.scaleBand()
      .domain(xLabels)
      .range([marginLeft, width - marginRight]);

    const y = d3.scaleLinear()
      .domain([0, 50])
      .range([height - marginBottom, marginTop]);

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height + 25);

    const keys = ['Senate', 'House of Representatives'];
    const color = d3.scaleOrdinal().domain(keys).range(['#00b894', '#a29bfe']);
    const iconSize = 20;

    svg.append('g')
      .selectAll('rect')
      .data(keys)
      .enter()
      .append('rect')
      .attr('x', marginLeft + 20)
      .attr('y', (d, i) => marginTop + i * (iconSize + 5))
      .attr('width', iconSize)
      .attr('height', iconSize)
      .style('fill', d => color(d));

    svg.append('g')
      .selectAll('text')
      .data(keys)
      .enter()
      .append('text')
      .attr('x', marginLeft + 45)
      .attr('y', (d, i) => marginTop + i * (20 + 5) + 15)
      .attr('width', 20)
      .attr('height', 20)
      .text(d => d)
      .style('font-size', '13px')
      .style('font-family', 'Arial');

    svg.append('text')
      .attr('x', width / 2 - 30)
      .attr('y', height + 20)
      .text('Age Range')
      .style('font-family', 'Arial');

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 20)
      .attr('x', -height / 2 - 35)
      .text('Years Served')
      .style('font-family', 'Arial');

    svg.append('g')
      .attr('transform', `translate(0,${height - marginBottom})`)
      .call(d3.axisBottom(x).ticks(6));

    svg.append('g')
      .attr('transform', `translate(${marginLeft},0)`)
      .call(d3.axisLeft(y).ticks(5));

    svg.append('g')
      .attr('fill', '#a29bfe')
      .selectAll()
      .data(yearsServedAverages)
      .join('rect')
      .attr('x', (d, i) => x(xLabels[i]))
      .attr('y', d => y(d[0]))
      .attr('stroke', 'black')
      .attr('stroke-width', 1)
      .attr('height', d => y(0) - y(d[0]))
      .attr('width', x.bandwidth());

    svg.append('g')
      .attr('fill', '#00b894')
      .selectAll()
      .data(yearsServedAverages)
      .join('rect')
      .attr('x', (d, i) => x(xLabels[i]))
      .attr('y', d => y(d[0] + d[1]))
      .attr('stroke', 'black')
      .attr('stroke-width', 1)
      .attr('height', d => y(d[0]) - y(d[0] + d[1]))
      .attr('width', x.bandwidth());
  });
</script>

<div bind:this={container}></div>
