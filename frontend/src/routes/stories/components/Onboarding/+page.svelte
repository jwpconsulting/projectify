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
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { ButtonAction } from "$lib/funabashi/types";

    let title = "Hello world";
    let prompt = "Choose your destiny";
    let nextLabel = "Continue now";
    const nextAction: ButtonAction = { kind: "a", href: "#" };
    let stepCount = 10;
    let step = 1;
</script>

<div class="flex flex-row">
    <h1>Onboarding Component Demo</h1>

    <div class="flex flex-col">
        <label>
            Title:
            <input type="text" bind:value={title} />
        </label>

        <label>
            Prompt:
            <input type="text" bind:value={prompt} />
        </label>

        <label>
            Next Label:
            <input type="text" bind:value={nextLabel} />
        </label>

        <label>
            Step Count:
            <input type="number" bind:value={stepCount} min="1" max="9999" />
        </label>

        <label>
            Current Step:
            <input type="number" bind:value={step} min="1" max="9999" />
        </label>
    </div>

    <div>
        <Onboarding {nextLabel} {nextAction} {stepCount} {step}>
            <span slot="title">{title}</span>
            <span slot="prompt">{prompt}</span>
        </Onboarding>
    </div>
</div>
