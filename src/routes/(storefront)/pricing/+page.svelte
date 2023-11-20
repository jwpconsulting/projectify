<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";

    $: features = [
        $_("pricing.features.list.feature-1"),
        $_("pricing.features.list.feature-2"),
        $_("pricing.features.list.feature-3"),
        $_("pricing.features.list.feature-4"),
        $_("pricing.features.list.feature-5"),
        $_("pricing.features.list.feature-6"),
        $_("pricing.features.list.feature-7"),
        $_("pricing.features.list.feature-8"),
        $_("pricing.features.list.feature-9"),
        $_("pricing.features.list.feature-10"),
        $_("pricing.features.list.feature-11"),
        $_("pricing.features.list.feature-12"),
        $_("pricing.features.list.feature-13"),
        $_("pricing.features.list.feature-14"),
    ];
</script>

<main class="flex w-full flex-col items-center py-10">
    <div class="flex w-full max-w-4xl flex-col items-center gap-8">
        <!-- explain that we have one price to rule them all -->
        <header class="flex w-full flex-col gap-4">
            <h1 class="text-center text-4xl font-bold sm:text-6xl">
                {$_("pricing.header.title")}
            </h1>
            <small class="text-center text-3xl font-bold">
                {$_("pricing.header.subtitle")}
            </small>
        </header>
        <!-- list the features -->
        <section class="flex flex-col gap-2">
            <h2 class="text-2xl">
                {$_("pricing.features.title")}
            </h2>
            <ul class="list-inside list-disc">
                {#each features as feature}
                    <li>{feature}</li>
                {/each}
            </ul>
        </section>
        <!-- colorful box with CTA -->
        <section
            class="flex w-full max-w-xl flex-col items-center gap-8 rounded-xl bg-background px-4 py-6"
        >
            <div class="flex flex-col gap-4">
                <h2 class="text-center text-xl font-bold">
                    {$_("pricing.plan")}
                </h2>
                <strong class="text-4xl font-bold">
                    {$_("pricing.price", { values: { price: 8 } })}
                </strong>
            </div>
            <Button
                action={{ kind: "a", href: "/user/sign-up" }}
                size="medium"
                color="blue"
                style={{ kind: "primary" }}
                label={$_("pricing.cta")}
            />
        </section>
    </div>
</main>
