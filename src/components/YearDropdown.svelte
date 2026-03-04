<script>
    import { onMount } from "svelte";
    import AgeComparisonChart from "./AgeComparisonChart.svelte";
    import { getMembersFromYear } from "../shared/getmembers.js";
    import { selectedYear, congressData, loadYear } from "./../shared/dataManager.js";

    // initialize available years (1995-2024)
    let options = [];
    for (let i = 1995; i < 2025; i++) options.push(i);

    // fetch initial data on client mount (delayed to ensure SSR-safe)
    onMount(async () => {
        console.log('YearDropdown onMount: calling loadYear for initial year', $selectedYear);
        awaitloadYear($selectedYear);
    });

</script>

<select value={$selectedYear} on:change={e => {
        const yr = +e.target.value;
        selectedYear.set(yr);
        if (typeof window !== 'undefined') loadYear(yr);
    }}>
    {#each options as option}
        <option value={option}>{option}</option>
    {/each}
</select>