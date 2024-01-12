<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2024 JWP Consulting GK

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
    // XXX totally duped from SelectLabelCheckBox
    import { Check } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import { getLabelColorClass, labelColors } from "$lib/utils/colors";

    export let chosenColor: string | undefined;
</script>

<div class="flex flex-col gap-2">
    <legend class="text-sm font-bold">
        {$_("dashboard.side-nav.filter-labels.color.prompt")}
    </legend>
    <div class="flex flex-row flex-wrap gap-3">
        {#each labelColors as color}
            <div class="group relative h-7 w-11">
                <input
                    type="radio"
                    name={color}
                    value={color}
                    bind:group={chosenColor}
                    class="absolute left-0 top-0 h-full w-full appearance-none rounded-2.5xl focus:border-base-content"
                />
                <div
                    class="flex h-full w-full flex-row items-center rounded-2.5xl border border-2 px-2.5 {getLabelColorClass(
                        'bg',
                        color,
                    )} {getLabelColorClass(
                        'border',
                        color,
                    )} {getLabelColorClass(
                        'bgHover',
                        color,
                    )} {getLabelColorClass('text', color)}"
                >
                    <div
                        class:visible={color === chosenColor}
                        class:invisible={color !== chosenColor}
                    >
                        <Icon src={Check} theme="outline" />
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
