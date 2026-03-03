<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { getMembersFromYear } from '../../shared/getmembers.js';

  let container;

  onMount(async () => {
    const width = 640;
    const height = 400;
    const marginTop = 20;
    const marginRight = 20;
    const marginBottom = 30;
    const marginLeft = 60;

    const year = 2024;
    const chamber = 'Senate';

    const data = await d3.json('/data/members.json');
    const filteredData = getMembersFromYear(chamber, year, data);

    const ages = filteredData.map(d => year - d.yob);
    const bin = d3.bin().domain([25, 110]).thresholds([31, 41, 51, 61, 71, 81]);
    const bins = bin(ages);

    const xLabels = bins.map((d, i) => {
      if (i === 0) return '<= 31';
      else if (i === bins.length - 1) return '> 80';
      else return `${d.x0}-${d.x1 - 1}`;
    });

    const x = d3.scaleBand()
      .domain(xLabels)
      .range([marginLeft, width - marginRight]);

    const y = d3.scaleLinear()
      .domain([0, chamber === 'Senate' ? 50 : 200])
      .range([height - marginBottom, marginTop]);

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height + 25);

    svg.append('text')
      .attr('x', width / 2 - 30)
      .attr('y', height + 20)
      .text('Age Range')
      .style('font-family', 'Arial');

    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 20)
      .attr('x', -height / 2 - 60)
      .text('Number of Members')
      .style('font-family', 'Arial');

    svg.append('g')
      .attr('transform', `translate(0,${height - marginBottom})`)
      .call(d3.axisBottom(x).ticks(6));

    svg.append('g')
      .attr('transform', `translate(${marginLeft},0)`)
      .call(d3.axisLeft(y).ticks(5));

    svg.append('g')
      .attr('fill', '#0984e3')
      .selectAll()
      .data(bins)
      .join('rect')
      .attr('x', (d, i) => x(xLabels[i]))
      .attr('y', d => y(d.length))
      .attr('stroke', 'black')
      .attr('stroke-width', 1)
      .attr('height', d => y(0) - y(d.length))
      .attr('width', x.bandwidth());
  });
</script>

<div bind:this={container}></div>
