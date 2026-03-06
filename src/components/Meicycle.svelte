<script>
  import PeopleRow from './PeopleRow.svelte';
  import MainKey from './MainKey.svelte';
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
  export let rowGap = 10; // vertical space between rows
  export let iconBase = 64;
  export let padding = 30; // passed through to PeopleRow

  let yearsServed = [];
  $: yearsServed = $congressData ? getYearsServed($selectedYear, $congressData) : [];
  $: peopleList = $congressData ? getMembersFromYear("Both", $selectedYear, $congressData) : [];
  $: totalPeople = peopleList.length;

  $: start = { r: 0x1a, g: 0x1a, b: 0x1a }; // black
    // const start = { r: 0x3e, g: 0x27, b: 0x23 }; // brown
    // const start = { r: 0x8b, g: 0x3a, b: 0x3a }; // auburn
  $: end = { r: 0xf5, g: 0xf5, b: 0xf5 }; // black / brown pairing
    // const end = { r: 0xe8, g: 0xe8, b: 0xe8 }; // auburn pairing

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
      for (let i = ci - 1; i >= 0; i--) counts[i] = counts[i + 1] + 1;
      for (let i = ci + 1; i < rcount; i++) counts[i] = counts[i - 1] - 1;
      // add remainder to furthest back row (index 0)
      // counts[0] += remainder;
      for (let i = 0; i < remainder; i++) {
        counts[i] += 1;
      }
    } else {
      // even: center two rows get ceil(avg) and floor(avg)
      const lowerCenter = rcount / 2; // index of lower center
      const upperCenter = lowerCenter - 1; // index of upper center
      counts[upperCenter] = Math.ceil(avg);
      counts[lowerCenter] = Math.floor(avg);
      // propagate up (towards back, decreasing index) adding 3
      for (let i = upperCenter - 1; i >= 0; i--) counts[i] = counts[i + 1] + 1;
      // propagate down (towards front, increasing index) subtracting 3
      for (let i = lowerCenter + 1; i < rcount; i++) counts[i] = counts[i - 1] - 1;
      // counts[0] += remainder;
      for (let i = 0; i < remainder; i++) {
        counts[i] += 1;
      }
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
  // $: console.log('Meicycle debug — selectedYear, totalPeople, numRows ->', $selectedYear, totalPeople, numRows);
  // $: console.log('Meicycle debug — computedRowCounts ->', computedRowCounts);
  // $: console.log('Meicycle debug — rowsPeople lengths ->', rowsPeople.map(r => r.length));
  // $: console.log('Meicycle debug — $congressData ->', $congressData);
  // console.log("Here comes the years served for the selected year:");
  // console.log(yearsServed);
  // console.log("Years served log ends here.");

  // parse thru the arrays 

</script>

<svg
  viewBox={`0 0 ${width} ${rowsPeople.length * rowHeight + (rowsPeople.length - 1) * rowGap}`}
  preserveAspectRatio="xMidYMid meet"
  style="overflow:visible; display:block; width:100%; height:auto; margin-bottom: 20px"
>
<!-- <path stroke="rgba(1,1,1,1)" stroke-linecap="miter" stroke-linejoin="miter" fill="none" pointer-events="none" d="M 10 240 Q 600 140 1190 240" stroke-width="76.8"></path> -->

  {#each rowsPeople as peopleRow, i}
    <g transform={`translate(0, ${i * (rowHeight + rowGap)})`}>
      <PeopleRow
        count={peopleRow.length}
        people={peopleRow}
        year={$selectedYear}
        width={width}
        height={rowHeight}
        iconBase={iconBase}
        padding={padding + i * 15}
        start={start}
        end={end}
        // client:load
      />
    </g>
  {/each}

<MainKey start={start} end={end} transform={`translate(${width / 2 - 600}, ${rowsPeople.length * (rowHeight + rowGap) + 170})`} />

</svg>


