<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let svg;

  const data = [10, 20, 30, 40];

  onMount(() => {
    const width = 400;
    const height = 200;

    const x = d3.scaleBand()
      .domain(data.map((d, i) => i))
      .range([0, width])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data)])
      .range([height, 0]);

    const chart = d3.select(svg)
      .attr("width", width)
      .attr("height", height);

    chart.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", (_, i) => x(i))
      .attr("y", d => y(d))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d));
  });
</script>

<svg bind:this={svg}></svg>