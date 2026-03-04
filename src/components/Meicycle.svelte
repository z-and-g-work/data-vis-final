<script>
  import PeopleRow from './PeopleRow.svelte';
  import { getMembersFromYear, getYearsServed } from "./../shared/getmembers.js";
  import { selectedYear, congressData } from "./../shared/dataManager.js";

  /**
   * Array of numbers representing how many icons per row.
   * The first element is the top/back row, last is front row.
   */
  export let rows = [10, 12, 14, 16];
  // number of rows to compute for the Meicycle; default to the length of the
  // `rows` array for backwards compatibility.
  export let numRows = rows.length;
  export let width = 900;
  export let rowHeight = 220;
  export let rowGap = 30; // vertical space between rows
  export let iconBase = 64;
  export let hairColor = '#fdcb6e';
  export let shirtColor = '#ff7675';
  export let skinColor = '#74b9ff';
  export let padding = 60; // passed through to PeopleRow

  let yearsServed = [];
  console.log("Congress Data: ", $congressData);
  $: yearsServed = $congressData ? getYearsServed($selectedYear, $congressData) : [];
  console.log(yearsServed);
  // list of people (both chambers) for the selected year
  $: peopleList = $congressData ? getMembersFromYear("Both", $selectedYear, $congressData) : [];
  console.log(peopleList);
  console.log("Selected year:", $selectedYear);
  $: totalPeople = peopleList.length;
  console.log("Total people for selected year:", totalPeople);

  function computeRowCounts(total, rcount) {
    if (rcount <= 0) return [];
    if (!total || total <= 0) return new Array(rcount).fill(0);
    const avg = total / rcount;
    const base = Math.floor(avg);
    const remainder = total - base * rcount;

    const counts = new Array(rcount).fill(0);

    if (rcount % 2 === 1) {
      // odd: center row = base; above center add 3 per step; below subtract 3 per step
      const ci = Math.floor(rcount / 2);
      counts[ci] = base;
      for (let i = ci - 1; i >= 0; i--) counts[i] = counts[i + 1] + 3;
      for (let i = ci + 1; i < rcount; i++) counts[i] = counts[i - 1] - 3;
      // add remainder to furthest back row (index 0)
      counts[0] += remainder;
    } else {
      // even: center two rows get ceil(avg) and floor(avg)
      const lowerCenter = rcount / 2; // index of lower center
      const upperCenter = lowerCenter - 1; // index of upper center
      counts[upperCenter] = Math.ceil(avg);
      counts[lowerCenter] = Math.floor(avg);
      // propagate up (towards back, decreasing index) adding 3
      for (let i = upperCenter - 1; i >= 0; i--) counts[i] = counts[i + 1] + 3;
      // propagate down (towards front, increasing index) subtracting 3
      for (let i = lowerCenter + 1; i < rcount; i++) counts[i] = counts[i - 1] - 3;
      counts[0] += remainder;
    }

    // ensure no negative counts; if negatives, shift min to 0 and redistribute
    const min = Math.min(...counts);
    if (min < 0) {
      const shift = -min;
      for (let i = 0; i < counts.length; i++) counts[i] += shift;
    }

    // final safety: if sum differs, adjust the back row
    const sum = counts.reduce((a, b) => a + b, 0);
    if (sum !== total) counts[0] += total - sum;

    return counts;
  }

  $: computedRowCounts = computeRowCounts(totalPeople, numRows);

  // slice peopleList into arrays per row: furthest back is index 0
  $: rowsPeople = (() => {
    const out = [];
    let cursor = 0;
    for (let i = 0; i < computedRowCounts.length; i++) {
      const c = Math.max(0, computedRowCounts[i] || 0);
      out.push(peopleList.slice(cursor, cursor + c));
      cursor += c;
    }
    return out;
  })();

  // Debug logs to help trace updates
  $: console.log('Meicycle debug — selectedYear, totalPeople, numRows ->', $selectedYear, totalPeople, numRows);
  $: console.log('Meicycle debug — computedRowCounts ->', computedRowCounts);
  $: console.log('Meicycle debug — rowsPeople lengths ->', rowsPeople.map(r => r.length));
  $: console.log('Meicycle debug — $congressData ->', $congressData);
  console.log("Here comes the years served for the selected year:");
  console.log(yearsServed);
  console.log("Years served log ends here.");

  // parse thru the arrays 

</script>

<svg
  width={width}
  height={rowsPeople.length * rowHeight + (rowsPeople.length - 1) * rowGap}
  style="overflow:visible; display:block"
>
  {#each rowsPeople as peopleRow, i}
    <g transform={`translate(0, ${i * (rowHeight + rowGap)})`}>
      <PeopleRow
        count={peopleRow.length}
        people={peopleRow}
        year={$selectedYear}
        width={width}
        height={rowHeight}
        iconBase={iconBase}
        padding={padding}
        hairColor={hairColor}
        shirtColor={shirtColor}
        skinColor={skinColor}
        client:load
      />
    </g>
  {/each}
</svg>
