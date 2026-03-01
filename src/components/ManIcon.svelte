<script>
    export let hairColor = "#fdcb6e";
    export let shirtColor = "#ff7675";
    export let skinColor = "#74b9ff";
    export let size = 40;
    // what part of the icon to render: "full", "body", or "head"
    export let part = "full";
</script>

<svg
    width={size}
    height={size}
    viewBox="0 0 200 200"
    xmlns="http://www.w3.org/2000/svg"
    {...$$restProps}
>
    {#if part === 'full' || part === 'head'}
      <circle cx="100" cy="70" r="35" fill={skinColor} />
      <path
          d="M65 60 Q100 1 135 60 Z"
          fill={hairColor}
      />
    {/if}
    {#if part === 'full' || part === 'body'}
      <rect x="75" y="105" width="50" height="70" rx="10" fill={shirtColor} />
      <rect x="45" y="110" width="30" height="15" rx="7" fill={shirtColor} />
      <rect x="125" y="110" width="30" height="15" rx="7" fill={shirtColor} />
    {/if}
</svg>