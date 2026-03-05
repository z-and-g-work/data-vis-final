<script>
    import "./../styles/style.css";
    
    let start = { r: 0x1a, g: 0x1a, b: 0x1a }; // black
    let end = { r: 0xf5, g: 0xf5, b: 0xf5 }; // black / brown pairing
    let ages = [30, 40, 50, 60, 70, 80];

</script>

<svg
    style="overflow:visible;"
    viewBox="0 0 1000 200"
    height=70px
    xmlns="http://www.w3.org/2000/svg"
    {...$$restProps}
>

    <defs>
        <linearGradient id="myGradient" gradientUnits="userSpaceOnUse" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="5%" stop-color={`rgb(${start.r}, ${start.g}, ${start.b})`} />
            <stop offset="95%" stop-color={`rgb(${end.r}, ${end.g}, ${end.b})`} />
        </linearGradient>

        <!-- Clip to only show bottom half of circles -->
        <clipPath id="bottomHalf">
            <rect x="0" y="60" width="1000" height="200" />
        </clipPath>

        <filter id="blur-again" x="-50%" y="-100%" width="200%" height="300%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" />
        </filter>
    </defs>

    <text
            x={500}
            y="-35"
            text-anchor="middle"
            font-size="80"
            fill="var(--text-subtitle)"
            font-family="var(--font-heading)"
            font-weight=400
        >
            Member Age
        </text>

    <!-- Semi-circles (bottom half only) with labels -->
    {#each ages as age, i}
        {@const cx = 100 + (age - 30) * (800 / (ages[ages.length-1] - ages[0]))}
        {@const r = Math.round(start.r + (end.r - start.r) * ((age - 30) / 50))}
        {@const g = Math.round(start.g + (end.g - start.g) * ((age - 30) / 50))}
        {@const b = Math.round(start.b + (end.b - start.b) * ((age - 30) / 50))}
        {@const color = `rgb(${r}, ${g}, ${b})`}

        <text
            x={cx}
            y="185"
            text-anchor="middle"
            font-size="64"
            fill="black"
            font-family="var(--font-heading)"
            font-weight=600
        >
            {age}
        </text>

        <path 
            d={`M ${cx - 70} 130 L ${cx - 70} -10 L ${cx + 70} -10 L ${cx + 70} 130 Z`}
            fill="rgba(158,94,12)"
        />

        <circle
            cx={cx}
            cy="60"
            r="50"
            fill={color}
        />

        <circle
            cx={cx}
            cy="60"
            r="50"
            fill="#74b9ff"
            clip-path="url(#bottomHalf)"
        />
    {/each}
</svg>