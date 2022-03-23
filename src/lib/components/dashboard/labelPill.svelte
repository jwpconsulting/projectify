<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";
    import IconClose from "../icons/icon-close.svelte";
    export let label;
    export let active = true;
    export let deleteIcon = false;
</script>

<div
    style="{`--color:${getColorFromInx(label.color).style}; --opacity:${
        active ? '1.0' : '0.2'
    }`};"
    class="label whitespace-nowrap font-bold text-xs px-3 py-1 rounded-full border max-w-xs"
>
    <span class="nowrap-ellipsis">{label.name}</span>
    {#if deleteIcon}
        <div
            class="relative flex justify-center items-center w-4 h-4 bg-current mr-[-8px] rounded-full ml-2"
        >
            <div class="text-[#fff] w-3 h-3 absolute top-[-1px]">
                <IconClose />
            </div>
        </div>
    {/if}
</div>
