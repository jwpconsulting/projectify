<script lang="ts">
    import type { FeatureDescription } from "$lib/types/ui";

    export let feature: FeatureDescription;
</script>

<div class="flex flex-col gap-6 sm:grid sm:grid-cols-2">
    <div
        class={`flex flex-col gap-12 ${
            feature.image.position === "left" ? "sm:order-last" : ""
        }`}
    >
        <h4 class="text-xl font-bold sm:mt-24 sm:text-4xl">
            {feature.header}
        </h4>
        <p class="text-l">
            {feature.text}
        </p>
    </div>
    <div class="min-w-full max-w-md">
        <img src={feature.image.src} alt={feature.image.alt} />
    </div>
</div>
