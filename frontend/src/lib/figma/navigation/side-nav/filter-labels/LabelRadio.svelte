<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    // XXX totally duped from SelectLabelCheckBox
    import { Check } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import {
        getLabelColorClass,
        labelColors,
        type LabelColor,
    } from "$lib/utils/colors";

    export let chosenColor: string | undefined;
    $: colorName = {
        orange: $_("dashboard.side-nav.filter-labels.color.colors.orange"),
        pink: $_("dashboard.side-nav.filter-labels.color.colors.pink"),
        blue: $_("dashboard.side-nav.filter-labels.color.colors.blue"),
        purple: $_("dashboard.side-nav.filter-labels.color.colors.purple"),
        yellow: $_("dashboard.side-nav.filter-labels.color.colors.yellow"),
        red: $_("dashboard.side-nav.filter-labels.color.colors.red"),
        green: $_("dashboard.side-nav.filter-labels.color.colors.green"),
    } satisfies Record<LabelColor, string>;
</script>

<div class="flex flex-col gap-2">
    <legend class="font-bold">
        {$_("dashboard.side-nav.filter-labels.color.prompt")}
    </legend>
    <div class="flex flex-row flex-wrap gap-3">
        {#each labelColors as color}
            <div class="group relative h-7 w-11">
                <label for="label-radio-{color}" class="sr-only"
                    >{colorName[color]}</label
                >
                <input
                    type="radio"
                    name={color}
                    id="label-radio-{color}"
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
