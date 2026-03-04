<script>
    import { onMount } from "svelte";
    import AgeComparisonChart from "./AgeComparisonChart.svelte";
    import { getMembersFromYear } from "../shared/getmembers.js";
    import { selectedYear, congressData, loadYear } from "./../shared/dataManager.js";
    import "../styles/timeline.css";

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

<div class="timeline-and-text-container">
    <p> Currently { $selectedYear } : { $selectedYear % 2 ? '1st' : '2nd' } half of congress { Math.ceil(( $selectedYear - 1788) / 2)} </p>
    <div class="timeline-container">
        {#each options as option}
            <button 
                type="button"
                class:active={$selectedYear === option}
                on:click={() => selectedYear.set(option)}
            >
                {option.toString().substring(2, 4)}
            </button>
        {/each}
    </div>
</div>