<script>

    import * as d3 from "d3";
    import {getMembersFromYear, getYearsServed} from "../shared/getmembers.js";
    import {onMount} from "svelte";
    import { selectedYear, congressData, loadYear } from "../shared/dataManager.js";

    //export let year;

    let svg;
    let mounted = false;

    async function createChart(data, year) {
        if (!data || !year) {
            console.log("data or year is null or undefined");
            return;
        };

        //first get rid of previous chart
        d3.select(svg).selectAll("*").remove();

        // Declare the chart dimensions and margins.
        const width = 640;
        const height = 400;
        const marginTop = 20;
        const marginRight = 20;
        const marginBottom = 30;
        const marginLeft = 60;

        const congressNumberThatYear = Math.ceil((year - 1788) / 2);

        //get all data from that year's congress
        // const data = await d3.json(`/public/data/by_congress/${congressNumberThatYear}.json`);
        //get members from specified year
        const houseFilteredData = getMembersFromYear("House of Representatives", year, data);
        const senateFilteredData = getMembersFromYear("Senate", year, data)
        //get the years members served in each chamber
        const houseYearsServed = getYearsServed(year, houseFilteredData);
        const senateYearsServed = getYearsServed(year, senateFilteredData);

        //sort members into bins based on age
        const bin = d3.bin().domain([25, 110]).thresholds([31, 41, 51, 61, 71, 81]).value(d => d[1]);
        const houseBins = bin(houseYearsServed);
        const senateBins = bin(senateYearsServed);

        //get average years served for each bin to use in chart
        const houseYearsServedAverages = [];
        const senateYearsServedAverages = [];
        houseBins.forEach(bin => {
            let totalYears = 0;
            bin.forEach(member => {
                totalYears += member[2] + member[3];
            })
            const averageYears = bin.length === 0 ? 0 : Math.round(totalYears / bin.length);
            houseYearsServedAverages.push(averageYears)
        })
        senateBins.forEach(bin => {
            let totalYears = 0;
            bin.forEach(member => {
                totalYears += member[2] + member[3];
            })
            const averageYears = bin.length === 0 ? 0 : Math.round(totalYears / bin.length);
            senateYearsServedAverages.push(averageYears)
        })

        //set names of each bin
        const xLabels = houseBins.map((d, i) => {
            if (i === 0) {
                return "25-30"
            } else if (i === houseBins.length - 1) {
                return "> 80"
            } else {
                return `${d.x0}-${d.x1 - 1}`
            }
        })

        const x = d3.scaleBand()
            .domain(xLabels)
            .range([marginLeft, width - marginRight]);

        const y = d3.scaleLinear()
            .domain([0, 50])
            .range([height - marginBottom, marginTop]);

        d3.select(svg)
            .attr("width", width + 500)
            .attr("height", height + 25);

        //create legend
        const keys = ["House of Representatives", "Senate"];
        const color = d3.scaleOrdinal().domain(keys).range(["#a29bfe", "#00b894"]);
        const iconSize = 20;
        d3.select(svg).append("g")
            .selectAll("rect")
            .data(keys)
            .enter()
            .append("rect")
            .attr("x", marginLeft + 20)
            .attr("y", (d, i) => {
                return marginTop + i * (iconSize + 5)
            })
            .attr("width", iconSize)
            .attr("height", iconSize)
            .style("fill", d => {
                return color(d)
            });

        d3.select(svg).append("g")
            .selectAll("text")
            .data(keys)
            .enter()
            .append("text")
            .attr("x", marginLeft + 45)
            .attr("y", (d, i) => {
                return marginTop + i * (20 + 5) + 15
            })
            .attr("width", 20)
            .attr("height", 20)
            .text(d => d)
            .style("font-size", "13px")
            .style("font-family", "Arial");

        //create labels
        d3.select(svg).append("text")
            .attr("x", width / 2 - 30)
            .attr("y", height + 20)
            .text("Age Range")
            .style("font-family", "Arial");

        d3.select(svg).append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 20)
            .attr("x", -height / 2 - 80)
            .text("Years Served in Congress")
            .style("font-family", "Arial");

        //create x axis
        d3.select(svg).append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(d3.axisBottom(x).ticks(6));

        //create y axis
        d3.select(svg).append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y).ticks(5));

        //create each house bar
        d3.select(svg).append("g")
            .attr("fill", "#a29bfe")
            .selectAll()
            .data(houseYearsServedAverages)
            .join("rect")
            .attr("x", (d, i) => x(xLabels[i]) + x.bandwidth() / 6)
            .attr("y", d => y(d))
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .attr("height", d => y(0) - y(d))
            .attr("width", x.bandwidth() / 3)

        //create each senate bar
        d3.select(svg).append("g")
            .attr("fill", "#00b894")
            .selectAll()
            .data(senateYearsServedAverages)
            .join("rect")
            .attr("x", (d, i) => x(xLabels[i]) + x.bandwidth() / 2)
            .attr("y", d => y(d))
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .attr("height", d => y(0) - y(d))
            .attr("width", x.bandwidth() / 3)
    }

    onMount(() => {
        mounted = true;
    })

    $: if (mounted && $congressData && $selectedYear) {
        createChart($congressData, $selectedYear);
    } else if (mounted && $selectedYear) {
        loadYear($selectedYear);
        createChart();
    }

</script>
<svg bind:this={svg}></svg>

<style>
    svg {
        display: block;
        margin: 0 auto;
    }
</style>