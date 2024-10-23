<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type {
        ButtonAction,
        ButtonStyle,
        ButtonColor,
    } from "$lib/funabashi/types";
    import { Plus } from "@steeze-ui/heroicons";

    const styles: ButtonStyle[] = [
        { kind: "primary" },
        { kind: "secondary" },
        { kind: "tertiary" },
        { kind: "tertiary", icon: { position: "left", icon: Plus } },
        { kind: "tertiary", icon: { position: "right", icon: Plus } },
    ];
    const colors: ButtonColor[] = ["blue", "red"];
    const actions: ButtonAction[] = [
        {
            kind: "button",
            action: () => {
                message = new Date().toISOString();
            },
        },
        { kind: "button", disabled: true },
        { kind: "submit" },
        { kind: "a", href: "#" },
    ];
    const labels = [
        "Primary",
        "Secondary",
        "Tertiary",
        "Tertiary with Left Icon",
        "Tertiary with Right Icon",
    ];

    const actionLabels = {
        button: "Button",
        submit: "Submit",
        a: "Anchor",
    };

    let message = "";
</script>

<div class="flex flex-col gap-8">
    <h1 class="text-4xl font-bold">Button Showcase</h1>
    <p>Last clicked: {message}</p>

    <div class="flex flex-col gap-6">
        {#each styles as style, index}
            <div class="flex flex-col gap-4">
                <h2 class="text-2xl font-semibold">{labels[index]}</h2>
                <div class="flex flex-col gap-4">
                    {#each actions as action}
                        <div class="flex gap-4">
                            {#each colors as color}
                                <Button
                                    label="{actionLabels[action.kind]} {color}"
                                    {style}
                                    {color}
                                    size="medium"
                                    {action}
                                />
                            {/each}
                        </div>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</div>
