<script>
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
            <rect x="0" y="220" width="1000" height="200" />
        </clipPath>

        <filter id="blur-again" x="-50%" y="-100%" width="200%" height="300%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" />
        </filter>
    </defs>
    
    <!-- blur top -->
    <path
        d={`M350 -40 L650 -40 L 650 10 L 350 10 Z`}
        fill="black"
        stroke="black"
        stroke-width=10
        stroke-linejoin="round"
        filter="url(#blur-again)"
    />

    <!-- blur main -->
    <path
        d={`M-40 0 L1040 0 L 1040 290 L -40 290 Z`}
        fill="black"
        stroke="black"
        stroke-width=10
        stroke-linejoin="round"
        filter="url(#blur-again)"
    />

    <!-- top border -->
    <path
        d={`M350 -40 L650 -40 L 650 10 L 350 10 Z`}
        fill="none"
        stroke="black"
        stroke-width=6
        stroke-linejoin="round"
    />

    <!-- main fill and border -->
    <path
        d={`M-30 0 L1040 0 L 1040 290 L -30 290 Z`}
        fill={"rgba(158,94,12)"}
        stroke="black"
        stroke-width=6
        stroke-linejoin="round"
    />

    <!-- top overwrite -->
    <path
        d={`M353 -37 L647 -37 L 647 10 L 353 10 Z`}
        // fill="none"
        fill={"rgba(158,94,12)"}
        // stroke="none"
        stroke-left="white"
        stroke-width=6
        stroke-linejoin="round"
    />

    <!-- color gradient -->
    <path
        d={`M60 80 L940 80`}
        stroke="url(#myGradient)"
        stroke-width=100
        stroke-linecap="round"
    />

    <text
        x=500
        y=10
        text-anchor="middle"
        font-size="48"
        fill="black"
        font-family="sans-serif"
        font-weight=600
        stroke='rgb(255,255,255,.5)'
        stroke-width=7
        paint-order="stroke"
    >
        Age Key
    </text>

    <!-- make color gradient only top half -->
    <path
        d={`M10 80 L990 80 L 990 150 L 10 150 Z`}
        fill="rgba(158,94,12)"
    />

    <!-- Semi-circles (bottom half only) with labels -->
    {#each ages as age, i}
        {@const cx = 100 + (age - 30) * (800 / (ages[ages.length-1] - ages[0]))}
        {@const r = Math.round(start.r + (end.r - start.r) * ((age - 30) / 50))}
        {@const g = Math.round(start.g + (end.g - start.g) * ((age - 30) / 50))}
        {@const b = Math.round(start.b + (end.b - start.b) * ((age - 30) / 50))}
        {@const color = `rgb(${r}, ${g}, ${b})`}
        
        <path 
            d={`M ${cx} 81 L ${cx} 100`}
            stroke="black"
            stroke-width=2
        />

        <text
            x={cx}
            y="140"
            text-anchor="middle"
            font-size="42"
            fill="black"
            font-family="sans-serif"
            font-weight=600
            stroke='rgb(255,255,255,.5)'
            stroke-width=7
            paint-order="stroke"
        >
            {age}
        </text>

        <path 
            d={`M ${cx} 150 L ${cx} 180`}
            stroke="black"
            stroke-width=2
        />

        <circle
            cx={cx}
            cy="220"
            r="50"
            fill={color}
        />

        <circle
            cx={cx}
            cy="220"
            r="50"
            fill="#74b9ff"
            clip-path="url(#bottomHalf)"
        />
    {/each}
</svg>