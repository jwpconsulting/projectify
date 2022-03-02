<script lang="ts">
    export let label;
    export let labelVAlign = "baseline";
</script>

<div
    class:items-baseline={labelVAlign === "baseline"}
    class:items-start={labelVAlign === "start"}
    class:items-center={labelVAlign === "center"}
    class="flex space-x-4 w-full pt-4 divide-x divide-base-300"
>
    <div class="flex font-bold w-[140px] px-2">
        <spna class="nowrap-ellipsis">{label}</spna>
    </div>
    <div class="flex grow px-2 pl-4">
        <slot />
    </div>
</div>
