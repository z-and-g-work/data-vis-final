<script>
    import { onMount } from "svelte";
    import AgeComparisonChart from "./AgeComparisonChart.svelte";
    import { getMembersFromYear } from "../shared/getmembers.js";
    import { selectedYear, congressData, loadYear } from "./../shared/dataManager.js";

    onMount(() => loadYear(2024));

    let options = [];

    for (let i = 1995; i < 2025; i++) {
        options.push(i)
    }

    let mounted = false;

    onMount(() => {
        mounted = true;
        loadYear($selectedYear);
    });

    $: if (mounted) loadYear($selectedYear);

</script>

<select bind:value={ $selectedYear }>
    {#each options as option}
        <option value={option}>{option}</option>
    {/each}
</select>