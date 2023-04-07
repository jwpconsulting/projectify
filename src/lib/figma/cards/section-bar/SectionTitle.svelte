<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ChevronDown, ChevronRight } from "@steeze-ui/heroicons";
    import type { SvelteComponent } from "svelte";
    import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";

    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    export let section: WorkspaceBoardSection;
    export let toggleOpen: () => void;
    export let open: boolean;

    let dropDownMenuBtnRef: SvelteComponent;

    function openDropDownMenu() {
        // TODO
        console.log("Need to open drop down menu at", dropDownMenuBtnRef);
    }
</script>

<header
    class="flex w-full flex-row items-center justify-between bg-foreground px-4 py-2"
>
    <div
        data-figma-name="Section header"
        class="flex min-w-0 shrink flex-row gap-4 text-base-content"
    >
        <button on:click={toggleOpen}>
            <Icon
                src={open ? ChevronDown : ChevronRight}
                class="h-6 w-6"
                theme="outline"
            />
        </button>
        <h1 class="nowrap-ellipsis min-w-0 shrink font-bold uppercase">
            {section.title}
        </h1>
    </div>
    <div class="flex shrink-0 flex-row gap-6" data-figma-name="Right side">
        <SquovalIcon
            action={{
                kind: "a",
                href: "#",
            }}
            icon="plus"
            state="active"
            active={false}
        />
        <SquovalIcon
            icon="ellipsis"
            state="active"
            active={false}
            bind:this={dropDownMenuBtnRef}
            action={{ kind: "button", action: openDropDownMenu }}
        />
    </div>
</header>
