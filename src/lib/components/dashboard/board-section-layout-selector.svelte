<script lang="ts">
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";

    import IconViewList from "../icons/icon-view-list.svelte";
    import IconViewBoards from "../icons/icon-view-boards.svelte";
    import { _ } from "svelte-i18n";
    import { getDropDown } from "../globalDropDown.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";
    import type { DashboardSectionsLayout } from "src/lib/types";

    function getLayoutIconFor(layout: DashboardSectionsLayout) {
        switch (layout) {
            case "columns":
                return IconViewBoards;
            case "list":
                return IconViewList;
        }
    }

    $: currentIcon = getLayoutIconFor($dashboardSectionsLayout);

    let targetBtn: HTMLElement | null = null;

    function openDropDownMenu() {
        if (!targetBtn) {
            throw new Error("Expected targetBtn");
        }
        let dropDownItems: DropDownMenuItem[] = [
            {
                id: "columns",
                label: "Columns",
                icon: IconViewBoards,
                onClick: () => {
                    dashboardSectionsLayout.set("columns");
                },
            },
            {
                id: "list",
                label: "List",
                icon: IconViewList,
                onClick: () => {
                    dashboardSectionsLayout.set("list");
                },
            },
        ];

        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, targetBtn, $dashboardSectionsLayout);
    }
</script>

<button
    bind:this={targetBtn}
    class="btn btn-ghost btn-xs flex h-10 shrink-0 items-center px-3"
    on:click={openDropDownMenu}
>
    <svelte:component this={currentIcon} />
    <span>{$_("layout")}</span>
</button>
