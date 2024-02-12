<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { SelectLabel } from "$lib/figma/types";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { deleteLabel } from "$lib/repository/workspace/label";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";

    export let label: SelectLabel;
    export let checked: boolean;

    export let onCheck: () => void;
    export let onUncheck: () => void;
    export let onEdit: (() => void) | undefined = undefined;

    function click() {
        checked = !checked;
        if (checked) {
            onCheck();
        } else {
            onUncheck();
        }
    }

    async function onDelete() {
        if (label.kind !== "label") {
            throw new Error("Expected label");
        }
        const l = label.label;
        await openDestructiveOverlay({ kind: "deleteLabel", label: l });
        await deleteLabel(l, { fetch });
    }
</script>

<button
    class="group flex w-full flex-row items-center justify-between px-5 hover:bg-base-200"
    on:click={click}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <SelectLabelCheckBox {label} bind:checked {onCheck} {onUncheck} />
        <div class="text-regular truncate text-sm">
            {#if label.kind === "allLabels"}
                {$_("filter-label.all")}
            {:else if label.kind === "noLabel"}
                {$_("filter-label.none")}
            {:else if label.kind === "label"}
                {label.label.name}
            {/if}
        </div>
    </div>
    <div class="flex flex-row items-center gap-2">
        {#if label.kind === "label" && onEdit}
            <CircleIcon
                size="small"
                icon="edit"
                action={{ kind: "button", action: onEdit }}
            />
            <CircleIcon
                size="small"
                icon="delete"
                action={{ kind: "button", action: onDelete }}
            />
        {/if}
    </div>
</button>
