<script>
  import { getYearsServed, getMembersYearsServed } from '../shared/getmembers';
  import ManIcon from './ManIcon.svelte';
  export let count = 7;
  export let altinator = false;
  // optional: array of person objects for this row. If provided, `count` will be derived
  // from `people.length`. Each person object should include at least a `yob` property.
  export let people = null;
  // pass the year so this component can compute ages if needed
  export let year = null;
  export let width = 800;
  export let height = 250;
  export let padding = 60;
  export let iconBase = 64;
  export let shirtColor = '#ff7675';
  export let skinColor = '#74b9ff';
  // export let skinColor = 'rgb(116,185,255,1)';
  export let skinColorSelected = '#bf392f';
  export let start = null;
  export let end = null;

  function testHairColorSet() {
    altinator = !altinator;
  }

  function scaleColor(age) {

    if (age <= 30) {
      return `rgb(${start.r}, ${start.g}, ${start.b})`;
    } 
    else if (age >= 80) {
      return `rgb(${end.r}, ${end.g}, ${end.b})`;
    }
    
    const r = Math.round(start.r + (end.r - start.r) * ((age - 30) / 50));
    const g = Math.round(start.g + (end.g - start.g) * ((age - 30) / 50));
    const b = Math.round(start.b + (end.b - start.b) * ((age - 30) / 50));

    return `rgb(${r}, ${g}, ${b})`;
  }

  function quadPoint(t, p0, p1, p2) {
    return {
      x: (1 - t) * (1 - t) * p0.x + 2 * (1 - t) * t * p1.x + t * t * p2.x,
      y: (1 - t) * (1 - t) * p0.y + 2 * (1 - t) * t * p1.y + t * t * p2.y,
    };
  }

  function computePositions(n) {
    const left = { x: padding, y: height - 20 };
    const right = { x: width - padding, y: height - 20 };
    const mid = { x: width / 2, y: height - 160 };
    const pts = [];
    if (n <= 0) {
      return [];
    }

    if (n === 1) {
      pts.push({ ...quadPoint(0.5, left, mid, right), t: 0.5 });
    } else {
      for (let i = 0; i < n; i++) {
        const t = i / (n - 1);
        pts.push({ ...quadPoint(t, left, mid, right), t});
      }
    }

    return pts.map((p) => {
      const ys = pts.map((p) => p.y);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const norm = (p.y - minY) / (maxY - minY || 1);
      const scale = 1.0 + norm * 0.2; // range ~0.6..1.2
      
      const tx = 2 * (1 - p.t) * (mid.x - left.x) + 2 * p.t * (right.x - mid.x);
      const ty = 2 * (1 - p.t) * (mid.y - left.y) + 2 * p.t * (right.y - mid.y);
      const angle = Math.atan2(ty, tx)

      return { ...p, scale, angle };
    });
  }

  $: positions = computePositions(people && people.length ? people.length : count);

  // $: console.log('PeopleRow debug — count, peopleLength, positionsLength ->', count, people && people.length, positions.length);

  // draw back-to-front: smaller y (higher on screen) first, larger y (closer) later
  $: drawOrder = positions
    .map((p, i) => ({ i, y: p.y }))
    .sort((a, b) => a.y - b.y)
    .map((o) => o.i);


  let isHovered = null;

</script>

<svg width={width} height={height} style="overflow:visible;">
  <defs>
    <filter id="dropShadow" x="0" y="0" width="200%" height="200%">
        <feDropShadow dx="5" dy="5" stdDeviation="4" flood-color="black" flood-opacity="0.5" />
    </filter>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="300%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="4" />
    </filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="8" />
    </filter>
  </defs>

  <!-- shadow of row -->
  <path
    d={`M ${padding - 25} ${height - 58} Q ${width / 2} ${height - 198} ${width - padding + 25} ${height - 58}`}
    // stroke="#9a5e0b"
    stroke="rgba(0,0,0)"
    // stroke="rgba(68,33,20,.9)"
    stroke-width={iconBase * .9}
    stroke-linecap="miter"
    stroke-linejoin="miter"
    fill="none"
    pointer-events="none"
    filter="url(#blur)"
  />

  <!-- thick quad ribbon overlay in front of the row to create a "stage" and cover bottom corners -->
  <path
    d={`M ${padding - 20} ${height - 60} Q ${width / 2} ${height - 200} ${width - padding +20} ${height - 60}`}
    // stroke="#9a5e0b"
    stroke="rgba(158,94,12)"
    // stroke="rgba(68,33,20,.9)"
    stroke-width={iconBase * .75}
    stroke-linecap="miter"
    stroke-linejoin="miter"
    fill="none"
    pointer-events="none"
  />

  <!-- yellow glow -->
  <path
    d={`M ${padding - 15} ${height - 55 - iconBase * .6 + 20} Q ${width / 2} ${height - 190 - iconBase * .6 + 20} ${width - padding + 15} ${height - 55 - iconBase * .6 + 20}`}
    stroke="#ffff00"
    stroke-width={6}
    stroke-linecap="miter"
    stroke-linejoin="miter"
    fill="none"
    pointer-events="none"
    filter="url(#glow)"
  />
  
  {#each drawOrder as idx}
    {#if positions[idx]}
      <g
              role="group" // just to avoid the yellow squigs
              on:mouseenter={() => isHovered = idx}
              on:mouseleave={() => isHovered = null}>
        <ManIcon
          part="head"
          size={iconBase * positions[idx].scale}
          x={positions[idx].x - (iconBase * positions[idx].scale) / 2}
          y={positions[idx].y - iconBase * positions[idx].scale}
          hairColor={scaleColor(year - people[idx].yob)}
          shirtColor={shirtColor}
          skinColor={isHovered === idx ? skinColorSelected : skinColor}
          yob={people && people[idx] ? people[idx].yob : null}
          age={people && people[idx] && year ? year - people[idx].yob : null}
          tilt={positions[idx].angle}
        />
      </g>
    {/if}
    {#if isHovered === idx}
      {@const hoverWidth = 160}
      {@const hoverHeight = 100}
      {@const x = Math.min(Math.max(positions[idx].x - hoverWidth / 2, 20), width - (hoverHeight + 80))}
      {@const y = positions[idx].y - 140 - Math.abs(positions[idx].x - (width - 40) / 2) * .05  }
      {@const yearsServed = getMembersYearsServed(year, people[idx])}
      <foreignObject x={x}  y={y} width={hoverWidth} height={hoverHeight} pointer-events="none">
        <div style="overflow:visible;background:#333;z-index:9999;color:white;padding:4px 8px;border-radius:4px;font-size:20px;text-align:center;">
          Age: {people && people[idx] ? year - people[idx].yob : null}<br/>
          House: {yearsServed.house} yrs<br/>
          Senate: {yearsServed.senate} yrs<br/>
        </div>
      </foreignObject>
    {/if}
  {/each}
</svg>
