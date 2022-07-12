<script lang="ts">
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";

    import IconViewList from "../icons/icon-view-list.svelte";
    import IconViewBoards from "../icons/icon-view-boards.svelte";
    import { _ } from "svelte-i18n";
    import { getDropDown } from "../globalDropDown.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";

    function getLayoutIconFor(layout: string) {
        switch (layout) {
            case "columns":
                return IconViewBoards;
            case "list":
                return IconViewList;
        }
    }

    $: currentIcon = getLayoutIconFor($dashboardSectionsLayout);

    let targetBtn = null;

    function openDropDownMenu() {
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

        getDropDown().open(dropDownItems, targetBtn, $dashboardSectionsLayout);
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
