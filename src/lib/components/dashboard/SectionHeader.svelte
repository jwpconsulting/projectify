<script lang="ts">
    import { _ } from "svelte-i18n";
    import { openNewTask } from "$lib/stores/dashboard";
    import type { DropDownMenuItem } from "$lib/components/globalDropDown.svelte";
    import { getDropDown } from "../globalDropDown.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import IconChevronRight from "../icons/icon-chevron-right.svelte";
    import IconSelector from "../icons/icon-selector.svelte";
    import IconClose from "../icons/icon-close.svelte";
    import IconArrowSUp from "../icons/icon-arrow-s-up.svelte";
    import IconArrowSDown from "../icons/icon-arrow-s-down.svelte";
    import { createEventDispatcher } from "svelte";
    import type { WorkspaceBoardSection } from "$lib/types";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { DotsHorizontal } from "@steeze-ui/heroicons";

    export let section: WorkspaceBoardSection;
    export let toggleOpen: () => void;
    export let open: boolean;
    export let isLast: boolean | null;
    export let isFirst: boolean | null;

    const dispatch = createEventDispatcher();

    $: openArrowDeg = open ? 90 : 0;
    let dropDownMenuBtnRef: HTMLElement;

    function openDropDownMenu() {
        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("expand-section"),
                icon: IconSelector,
                hidden: open,
                onClick: () => {
                    open = true;
                },
            },
            {
                label: $_("collapse-section"),
                icon: IconClose,
                hidden: !open,
                onClick: () => {
                    open = false;
                },
            },
            {
                label: $_("switch-with-previous-section"),
                icon: IconArrowSUp,
                hidden: isFirst === true,
                onClick: () => {
                    dispatch("switchWithPrevSection", { section });
                },
            },
            {
                label: $_("switch-with-next-section"),
                icon: IconArrowSDown,
                hidden: isLast === true,
                onClick: () => {
                    dispatch("switchWithNextSection", { section });
                },
            },
            {
                label: $_("add-task"),
                icon: IconPlus,
                onClick: () => {
                    openNewTask(section.uuid);
                },
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, dropDownMenuBtnRef);
    }
</script>

<header
    class:open
    class="sticky -top-2 z-10 flex flex-row items-center justify-between bg-base-100 px-4 py-2"
>
    <button class="flex flex-row gap-4" on:click={toggleOpen}>
        <div
            class="px-2 transition-transform"
            style="transform: rotate({openArrowDeg}deg);"
        >
            <IconChevronRight />
        </div>
        <div class="grid grow text-base font-bold uppercase">
            <span class="nowrap-ellipsis">
                {section.title}
                {#if section.tasks}
                    ({section.tasks.length})
                {/if}
            </span>
        </div>
    </button>
    <button
        bind:this={dropDownMenuBtnRef}
        on:click|stopPropagation={openDropDownMenu}
        class="p-1"
    >
        <Icon
            src={DotsHorizontal}
            theme="outline"
            class="h-6 w-6 text-base-content"
        />
    </button>
</header>

<style lang="scss">
    header {
        &::after {
            content: "";
            position: absolute;

            height: 1px;
            @apply bottom-0 left-3 right-3 bg-base-300;
            transition: all 300ms ease-in-out;
            opacity: 0;
        }

        &.open {
            &::after {
                opacity: 1;
            }
        }
    }
</style>
