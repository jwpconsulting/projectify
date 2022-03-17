<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";
    export let label;
    export let active = true;
</script>

<div
    style="{`--color:${getColorFromInx(label.color).style}; --opacity:${
        active ? '1.0' : '0.2'
    }`};"
    class="max-w-min label whitespace-nowrap font-bold text-xs px-3 py-1 m-1 rounded-full border"
>
    {label.name}
</div>
