<script>

    import * as d3 from "d3";
    import {getMembersFromYear} from "../shared/getmembers.js";
    import {onMount} from "svelte";

    export let year;
    export let chamber;

    let container;
    let svg;

    async function createChart() {
        //first get rid of previous chart
        d3.select(svg).selectAll("*").remove();

        //set dimensions and margins
        const width = 640;
        const height = 400;
        const marginTop = 20;
        const marginRight = 20;
        const marginBottom = 30;
        const marginLeft = 60;

        const congressNumberThatYear = Math.ceil((year - 1788) / 2);
        console.log(congressNumberThatYear);

        //get all data from that year's congress
        const data = await d3.json(`/public/data/by_congress/${congressNumberThatYear}.json`);
        //get members from specified year
        const filteredData = getMembersFromYear(chamber, year, data);

        //get ages of each member and sort them into bins
        const ages = filteredData.map(d => year - d.yob)
        const bin = d3.bin().domain([25, 110]).thresholds([31, 41, 51, 61, 71, 81]);
        const bins = bin(ages);

        //set names of each bin
        const xLabels = bins.map((d, i) => {
            if (i === 0) {
                return "<= 31"
            }
            else if (i === bins.length - 1) {
                return "> 80"
            }
            else {
                return `${d.x0}-${d.x1 - 1}`}
        })

        const x = d3.scaleBand()
            .domain(xLabels)
            .range([marginLeft, width - marginRight]);

        const y = d3.scaleLinear()
            .domain([0, (chamber === "Senate" ? 50 : 200)])
            .range([height - marginBottom, marginTop]);

        d3.select(svg)
            .attr("width", width)
            .attr("height", height + 25);

        //create labels
        d3.select(svg).append("text")
            .attr("x", width/2 - 30)
            .attr("y", height + 20)
            .text("Age Range")
            .style("font-family", "Arial");

        d3.select(svg).append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 20)
            .attr("x", -height/2 - 60)
            .text("Number of Members")
            .style("font-family", "Arial");

        //create x axis
        d3.select(svg).append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(d3.axisBottom(x).ticks(6));

        //create y axis
        d3.select(svg).append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y).ticks(5));

        //create each bar
        d3.select(svg).append("g")
            .attr("fill", (chamber === "Senate" ? "#00b894" : "#a29bfe"))
            .selectAll()
            .data(bins)
            .join("rect")
            .attr("x", (d, i) => x(xLabels[i]))
            .attr("y", d => y(d.length))
            .attr("stroke", "black")

            .attr("stroke-width", 1)
            .attr("height", d => y(0) - y(d.length))
            .attr("width", x.bandwidth())
    }

    let mounted = false;

    onMount(() => {
        createChart();
        mounted = true;
    })

    $: if (mounted && year) {
        createChart();
    }

</script>
<svg bind:this={svg}></svg>