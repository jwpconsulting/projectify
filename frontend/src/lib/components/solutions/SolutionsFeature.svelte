<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { FeatureDescription } from "$lib/types/ui";

    export let feature: FeatureDescription;
</script>

<section class="flex flex-col items-center gap-6 sm:grid sm:grid-cols-2">
    <div
        class={`flex flex-col gap-6 ${
            feature.image.position === "left" ? "sm:order-last" : ""
        }`}
    >
        <h4 class="text-xl font-bold sm:text-4xl">
            {feature.title}
        </h4>
        <p class="text-l">
            {feature.text}
        </p>
        {#if feature.learnMore !== undefined}
            <Anchor
                label={feature.learnMore.label}
                href={feature.learnMore.href}
            />
        {/if}
    </div>
    <div class="w-full max-w-xs justify-self-center">
        <enhanced:img src={feature.image.src} alt={feature.image.alt} />
    </div>
</section>
