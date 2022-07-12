<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";
    import IconClose from "../icons/icon-close.svelte";
    import type { Label } from "$lib/types";
    export let label: Label;
    export let active = false;
    export let deleteIcon = false;
    export let size: "sm" | "md" = "md";
</script>

<div
    style="{`--color:${getColorFromInx(label.color).style};`};"
    class:active
    class="label max-w-xs whitespace-nowrap rounded-full border px-3 py-1 text-xs font-bold"
    class:label-pill-sm={size === "sm"}
>
    <span class="nowrap-ellipsis">{label.name}</span>
    {#if deleteIcon}
        <div
            class="relative mr-[-8px] ml-2 flex h-4 w-4 items-center justify-center rounded-full bg-current"
        >
            <div class="absolute top-[-1px] h-3 w-3 text-[#fff]">
                <IconClose />
            </div>
        </div>
    {/if}
</div>

<style lang="scss">
    .label-pill-sm {
        @apply px-2 py-0;
        > span {
            font-size: 0.6rem;
        }
    }

    .label {
        &.active {
            @apply border bg-current;
            border-color: #fff;
            box-shadow: currentColor 0 0 0px 1px;
            > span {
                color: #fff;
            }
        }
    }
</style>
