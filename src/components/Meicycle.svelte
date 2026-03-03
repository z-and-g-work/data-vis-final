<script>
  import PeopleRow from './PeopleRow.svelte';
  import { getMembersFromYear, getYearsServed } from "./../shared/getmembers.js";
  import { selectedYear, congressData } from "./../shared/dataManager.js";

  /**
   * Array of numbers representing how many icons per row.
   * The first element is the top/back row, last is front row.
   */
  export let rows = [10, 12, 14, 16];
  export let width = 900;
  export let rowHeight = 220;
  export let rowGap = 30; // vertical space between rows
  export let iconBase = 64;
  export let hairColor = '#fdcb6e';
  export let shirtColor = '#ff7675';
  export let skinColor = '#74b9ff';
  export let padding = 60; // passed through to PeopleRow

  $: yearsServed = $congressData ? getYearsServed($selectedYear, $congressData) : [];

  console.log(yearsServed);

  // parse thru the arrays 

</script>

<svg
  width={width}
  height={rows.length * rowHeight + (rows.length - 1) * rowGap}
  style="overflow:visible; display:block"
>
  {#each rows as count, i}
    <g
      transform={`translate(0, ${i * (rowHeight + rowGap)})`}
    >
      <PeopleRow
        count={count}
        width={width}
        height={rowHeight}
        iconBase={iconBase}
        padding={padding}
        hairColor={hairColor}
        shirtColor={shirtColor}
        skinColor={skinColor}
      />
    </g>
  {/each}
</svg>
