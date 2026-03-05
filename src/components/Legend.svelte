<script>
    import ManIcon from '../components/ManIcon.svelte';

    import {getMembersYearsServed} from "../shared/getmembers.js";
    const ages = [30, 40, 50, 60, 70, 80]

    export let iconBase = 125;
    export let shirtColor = '#ff7675';
    export let skinColor = '#74b9ff';

    let part="head";
    let size = iconBase;
    let tilt=0;

    const alpha = Math.asin(10 / 90);

    $: x1 = 100 + 35 * Math.cos(Math.PI + alpha + tilt);
    $: y1 = 70  + 35 * Math.sin(Math.PI + alpha + tilt);
    $: x2 = 100 + 35 * Math.cos(-alpha + tilt);
    $: y2 = 70  + 35 * Math.sin(-alpha + tilt);
    $: rotation = tilt * (180 / Math.PI); // svg doesnt like radians, only degrees


    function scaleColor(age) {
        const start = { r: 0x1a, g: 0x1a, b: 0x1a }; // black
        // const start = { r: 0x3e, g: 0x27, b: 0x23 }; // brown
        // const start = { r: 0x8b, g: 0x3a, b: 0x3a }; // auburn
        const end = { r: 0xf5, g: 0xf5, b: 0xf5 }; // black / brown pairing
        // const end = { r: 0xe8, g: 0xe8, b: 0xe8 }; // auburn pairing

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
</script>

<div class="legend">
    <h3 class="legend-title">Member Age</h3>
    <div class="legend-items">
        {#each ages as age}
            <div class="legend-icons">
                <svg
                        style="overflow:visible;"
                        width={size}
                        height={size}
                        viewBox="0 0 200 200"
                        xmlns="http://www.w3.org/2000/svg"
                        {...$$restProps}
                >
                    {#if part === 'full' || part === 'head'}
                        <circle cx="100" cy="70" r="35" fill={skinColor}  />
                        <path
                                d={`M${x1} ${y1} A35 32 ${rotation} 1 1 ${x2} ${y2} Z`}
                                fill={scaleColor(age)}
                        />
                    {/if}
                </svg>
                <p class="legend-label">{age}</p>
            </div>
        {/each}
    </div>
</div>