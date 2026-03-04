<script>
    import * as d3 from "d3";
    import {onMount} from "svelte";

    export let hairColor = "#fdcb6e";
    export let shirtColor = "#ff7675";
    export let skinColor = "#74b9ff";
    export let size = 40;
    // what part of the icon to render: "full", "body", or "head"
    export let part = "full";

    export let x = 0;
    export let y = 0;

    let svg;
    function createManIcon() {
        //first get rid of previous man
        d3.select(svg).selectAll("*").remove();

        const manIcon = d3.select(svg)
            // .attr("width", size)
            // .attr("height", size)
            // .attr("viewBox", "0 0 200 200")
            // .attr("xmlns", "http://www.w3.org/2000/svg")
            // .attr("x", x)
            // .attr("y", y)
            .attr("transform", `translate(${x}, ${y}) scale(${size / 200})`)
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .append("g")
            .style("cursor", "pointer");

        if (part === 'full' || part === 'head') {
            manIcon.append("circle")
                .attr("cx", 100)
                .attr("cy", 70)
                .attr("r", 35)
                .attr("fill", skinColor)

            manIcon.append("path")
                .attr("d", "M65 60 Q100 1 135 60 Z")
                .attr("fill", hairColor)
        }
        if (part === "full" || part === "body") {
            manIcon.append("rect")
                .attr("x", 75)
                .attr("y", 105)
                .attr("width", 50)
                .attr("height", 70)
                .attr("rx", 10)
                .attr("fill", shirtColor)

            manIcon.append("rect")
                .attr("x", 45)
                .attr("y", 110)
                .attr("width", 30)
                .attr("height", 15)
                .attr("rx", 7)
                .attr("fill", shirtColor)

            manIcon.append("rect")
                .attr("x", 125)
                .attr("y", 110)
                .attr("width", 30)
                .attr("height", 15)
                .attr("rx", 7)
                .attr("fill", shirtColor)
        }

        // //create data on hover
        // const hoverBar = d3.select(svg)
        //     .append("g")
        //     .style("display", "none")
        //     .attr("pointer-events", "none");
        //
        // hoverBar.append("rect")
        //     .attr("width", 120)
        //     .attr("height", 50)
        //     .attr("rx", 6)
        //     .attr("fill", "#333");
        //
        // hoverBar.append("text")
        //     .attr("x", 60)
        //     .attr("y", 20)
        //     .attr("text-anchor", "middle")
        //     .attr("fill", "white")
        //     .attr("font-size", 10)
        //     .text("Age: 72");
        //
        // manIcon.on("mouseenter", function () {
        //     hoverBar.attr("transform", `translate(${x + 40}, ${y - 20}), scale(${1})`)
        //         .style("display", null)
        //     })
        //     .on("mouseleave", function () {
        //         hoverBar.style("display", "none")
        //     })
    }

    onMount(createManIcon)

</script>


<svg bind:this={svg}></svg>

<!--<svg-->
<!--    width={size}-->
<!--    height={size}-->
<!--    viewBox="0 0 200 200"-->
<!--    xmlns="http://www.w3.org/2000/svg"-->
<!--    {...$$restProps}-->
<!--&gt;-->
<!--    {#if part === 'full' || part === 'head'}-->
<!--      <circle cx="100" cy="70" r="35" fill={skinColor} />-->
<!--      <path-->
<!--          d="M65 60 Q100 1 135 60 Z"-->
<!--          fill={hairColor}-->
<!--      />-->
<!--    {/if}-->
<!--    {#if part === 'full' || part === 'body'}-->
<!--      <rect x="75" y="105" width="50" height="70" rx="10" fill={shirtColor} />-->
<!--      <rect x="45" y="110" width="30" height="15" rx="7" fill={shirtColor} />-->
<!--      <rect x="125" y="110" width="30" height="15" rx="7" fill={shirtColor} />-->
<!--    {/if}-->
<!--</svg>-->