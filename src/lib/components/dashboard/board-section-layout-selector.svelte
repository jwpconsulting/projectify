<script lang="ts">
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";

    import DropDownMenu from "../dropDownMenu.svelte";
    import IconViewGrid from "../icons/icon-view-grid.svelte";
    import IconViewList from "../icons/icon-view-list.svelte";
    import { _ } from "svelte-i18n";

    function getLayoutIconFor(layout) {
        switch (layout) {
            case "grid":
                return IconViewGrid;
            case "list":
                return IconViewList;
        }
    }

    $: currentIcon = getLayoutIconFor($dashboardSectionsLayout);
</script>

<DropDownMenu
    items={[
        {
            label: "Grid",
            icon: IconViewGrid,
            onClick: () => {
                dashboardSectionsLayout.set("grid");
            },
        },
        {
            label: "List",
            icon: IconViewList,
            onClick: () => {
                dashboardSectionsLayout.set("list");
            },
        },
    ]}
>
    <button
        tabindex="0"
        class="btn btn-ghost btn-xs flex h-10 shrink-0 items-center px-3"
    >
        <svelte:component this={currentIcon} />
        <span>{$_("layout")}</span>
    </button>
</DropDownMenu>
