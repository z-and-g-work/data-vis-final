<script>
    import ManIcon from '../components/ManIcon.svelte';

    import {getMembersYearsServed} from "../shared/getmembers.js";
    const positions = [{x: -20, y:0, age: 30}, {x: 40, y:0, age: 40}, {x: 80, y:0, age: 50}, {x: 120, y:0, age: 60}, {x: 200, y:0, age: 70}, {x: 200, y:0, age: 80}]

    export let iconBase = 125;
    export let shirtColor = '#ff7675';
    export let skinColor = '#74b9ff';


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
        {#each positions as idx}
            <div class="legend-icons">
                <ManIcon
                        part="head"
                        size={iconBase}
                        hairColor={scaleColor(idx.age)}
                        shirtColor={shirtColor}
                        skinColor={skinColor}
                        yob={idx.age}
                        age={idx.age}
                        tilt={0}
                />
                <p class="legend-label">{idx.age}</p>
            </div>
        {/each}
    </div>
</div>