<script>
    import AgeComparisonChart from "./AgeComparisonChart.svelte";

    let selectedYear = 2024;
    let options = [];
    for (let i = 1995; i < 2025; i++) {
        options.push(i)
    }
</script>

<select bind:value={selectedYear}>
    {#each options as option}
        <option value={option}>{option}</option>
    {/each}
</select>

<AgeComparisonChart {selectedYear} />