<script>
    import AgeComparisonChart from "./AgeComparisonChart.svelte";
    import YearsServedChart from "./YearsServedChart.svelte";

    let year = 2024;
    let options = [];
    for (let i = 1995; i < 2025; i++) {
        options.push(i)
    }
</script>

<select bind:value={year}>
    {#each options as option}
        <option value={option}>{option}</option>
    {/each}
</select>

<YearsServedChart {year} />
<AgeComparisonChart chamber={"Senate"} {year} />
<AgeComparisonChart chamber={"House of Representatives"} {year} />