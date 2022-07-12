<script lang="ts">
    export let label: string;
    export let labelVAlign = "baseline";
</script>

<div
    class:items-baseline={labelVAlign === "baseline"}
    class:items-start={labelVAlign === "start"}
    class:items-center={labelVAlign === "center"}
    class="flex w-full space-x-4 divide-x divide-base-300 pt-4"
>
    <div class="flex w-[140px] px-2 font-bold">
        <spna class="nowrap-ellipsis">{label}</spna>
    </div>
    <div class="flex grow px-2 pl-4">
        <slot />
    </div>
</div>
