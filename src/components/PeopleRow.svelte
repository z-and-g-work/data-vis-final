<script>
  import ManIcon from './ManIcon.svelte';
  export let count = 7;
  // optional: array of person objects for this row. If provided, `count` will be derived
  // from `people.length`. Each person object should include at least a `yob` property.
  export let people = null;
  // pass the year so this component can compute ages if needed
  export let year = null;
  export let width = 800;
  export let height = 250;
  export let padding = 60;
  export let iconBase = 64;
  export let hairColor = '#fdcb6e';
  export let shirtColor = '#ff7675';
  export let skinColor = '#74b9ff';

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
      pts.push(quadPoint(0.5, left, mid, right));
    } else {
      for (let i = 0; i < n; i++) {
        const t = i / (n - 1);
        pts.push(quadPoint(t, left, mid, right));
      }
    }

    const ys = pts.map((p) => p.y);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    return pts.map((p) => {
      const norm = (p.y - minY) / (maxY - minY || 1);
      const scale = 0.6 + norm * 0.6; // range ~0.6..1.2
      return { ...p, scale };
    });
  }

  $: positions = computePositions(people && people.length ? people.length : count);

  $: console.log('PeopleRow debug — count, peopleLength, positionsLength ->', count, people && people.length, positions.length);

  // draw back-to-front: smaller y (higher on screen) first, larger y (closer) later
  $: drawOrder = positions
    .map((p, i) => ({ i, y: p.y }))
    .sort((a, b) => a.y - b.y)
    .map((o) => o.i);
</script>

<svg width={width} height={height} style="overflow:visible; display:block">
  {#each drawOrder as idx}
    {#if positions[idx]}
      <g>
        <ManIcon
          part="body"
          size={iconBase * positions[idx].scale}
          x={positions[idx].x - (iconBase * positions[idx].scale) / 2}
          y={positions[idx].y - iconBase * positions[idx].scale}
          hairColor={hairColor}
          shirtColor={shirtColor}
          skinColor={skinColor}
          yob={people && people[idx] ? people[idx].yob : null}
          age={people && people[idx] && year ? year - people[idx].yob : null}
        />
      </g>
    {/if}
  {/each}

  <!-- thick quad ribbon overlay in front of the row to create a "stage" and cover bottom corners -->
  <path
    d={`M ${padding} ${height - 20} Q ${width / 2} ${height - 120} ${width - padding} ${height - 20}`}
    stroke="rgba(0,0,0,0.8)"
    stroke-width={iconBase * 1.2}
    stroke-linecap="round"
    stroke-linejoin="round"
    fill="none"
    pointer-events="none"
  />

  {#each drawOrder as idx}
    {#if positions[idx]}
      <g>
        <ManIcon
          part="head"
          size={iconBase * positions[idx].scale}
          x={positions[idx].x - (iconBase * positions[idx].scale) / 2}
          y={positions[idx].y - iconBase * positions[idx].scale}
          hairColor={hairColor}
          shirtColor={shirtColor}
          skinColor={skinColor}
          yob={people && people[idx] ? people[idx].yob : null}
          age={people && people[idx] && year ? year - people[idx].yob : null}
        />
      </g>
    {/if}
  {/each}
</svg>
