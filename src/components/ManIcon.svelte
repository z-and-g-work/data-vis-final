<script>
    export let hairColor = "#fdcb6e";
    export let shirtColor = "#ff7675";
    export let skinColor = "#74b9ff";
    export let size = 40;
    // what part of the icon to render: "full", "body", or "head"
    export let part = "full";
    export let tilt = 0;

    const alpha = Math.asin(10 / 90); 

    $: x1 = 100 + 35 * Math.cos(Math.PI + alpha + tilt);
    $: y1 = 70  + 35 * Math.sin(Math.PI + alpha + tilt);
    $: x2 = 100 + 35 * Math.cos(-alpha + tilt);
    $: y2 = 70  + 35 * Math.sin(-alpha + tilt);

    // to avoid fliter/gradient collisions
    let uid = Math.random().toString(36).slice(2, 7);
    $: direction = tilt < 0 ? 1 : -1;
    // console.log(tilt);

    $: rotation = tilt * (180 / Math.PI); // svg doesnt like radians, only degrees
    $: shadowDx = direction * 7 + -tilt * 30;                      
    $: shadowDy = Math.abs(Math.sin(tilt)) * 8;    

</script>

<defs>
    <filter id="dropShadow" x="0" y="0" width="200%" height="200%">
        <feDropShadow dx="5" dy="5" stdDeviation="4" flood-color="black" flood-opacity="0.5" />
    </filter>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="15" />
    </filter>
</defs>

<svg
    style="overflow:visible;"
    width={size}
    height={size}
    viewBox="0 0 200 200"
    xmlns="http://www.w3.org/2000/svg"
    {...$$restProps}
>
    {#if part === 'full' || part === 'head'}    
        <defs>
            <radialGradient id="shadowGrad_{uid}">
                <stop offset="0%"   stop-color="black" stop-opacity="1" />
                <stop offset="100%" stop-color="black" stop-opacity=".3" />
            </radialGradient>
            <filter id="shadowBlur_{uid}" x="-50%" y="-50%" width="500%" height="500%">
                <feGaussianBlur stdDeviation="6" />
            </filter>
        </defs>

        <circle cx={100 + shadowDx * 1.2 } cy={70 + shadowDy * 1.5} r="35" fill="url(#shadowGrad_{uid})" filter="url(#shadowBlur_{uid})"  />
        
        <circle cx="100" cy="70" r="35" fill={skinColor}  />
        <path
            d={`M${x1} ${y1} A35 32 ${rotation} 1 1 ${x2} ${y2} Z`}
            fill={hairColor}
      />
    {/if}
    {#if part === 'full' || part === 'body'}
      <rect x="75" y="105" width="50" height="70" rx="10" fill={shirtColor} />
      <rect x="45" y="110" width="30" height="15" rx="7" fill={shirtColor} />
      <rect x="125" y="110" width="30" height="15" rx="7" fill={shirtColor} />
    {/if}
</svg>