<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    import { _, json } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { aboutYouUrl } from "$lib/urls/onboarding";

    $: promptLines = $json("onboarding.welcome.prompt") as string[];
</script>

<Onboarding nextAction={{ kind: "a", href: aboutYouUrl }}>
    <svelte:fragment slot="title"
        >{$_("onboarding.welcome.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {#each promptLines as promptLine}
            <p>{promptLine}</p>
        {/each}
        <Anchor
            size="large"
            href="/pricing#trial-mode"
            label={$_("onboarding.welcome.help.trial-mode-features")}
        />
    </svelte:fragment>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
