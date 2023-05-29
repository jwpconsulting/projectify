<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
    import Button from "$lib/funabashi/buttons/Button.svelte";

    $: features = [
        $_("pricing-page.feature-1"),
        $_("pricing-page.feature-2"),
        $_("pricing-page.feature-3"),
        $_("pricing-page.feature-4"),
        $_("pricing-page.feature-5"),
        $_("pricing-page.feature-6"),
        $_("pricing-page.feature-7"),
        $_("pricing-page.feature-8"),
        $_("pricing-page.feature-9"),
        $_("pricing-page.feature-10"),
        $_("pricing-page.feature-11"),
        $_("pricing-page.feature-12"),
        $_("pricing-page.feature-13"),
        $_("pricing-page.feature-14"),
    ];
</script>

<main class="flex flex-col gap-20 bg-base-100">
    <header class="mt-8 text-center">
        <h1 class="mb-4 text-4xl font-bold sm:text-6xl">
            {$_("pricing-page.header")}
        </h1>
        <small class="sm-text-3xl text-3xl font-bold">
            {$_("pricing-page.subtitle")}
        </small>
    </header>
    <section class="space-y-8 text-center font-bold">
        <p class="text-2xl">
            {$_("pricing-page.feature-title")}
        </p>
        <div class="flex justify-center text-xl">
            <ul>
                {#each features as feature}
                    <li class="ml-10 flex flex-row items-center gap-4">
                        <Icon
                            src={Check}
                            theme="outline"
                            class="h-4 w-4 text-base-content"
                        />
                        {feature}
                    </li>
                {/each}
            </ul>
        </div>
    </section>
    <section
        class="m-4 grid grid-cols-1 gap-4 bg-base-200 p-12 sm:m-16 sm:grid-cols-3"
    >
        <strong class="text-center text-3xl font-bold">
            {$_("pricing-page.plan")}
        </strong>
        <div class="flex flex-row justify-center gap-4">
            <strong class="text-5xl font-bold">
                {$_("pricing-page.price")}
            </strong>
            <div class="flex flex-col justify-center">
                <div>
                    {$_("pricing-page.seat-per-month.seat")}
                    {$_("pricing-page.seat-per-month.per")}
                </div>
                <div>
                    {$_("pricing-page.seat-per-month.month")}
                </div>
            </div>
        </div>
        <Button
            action={{ kind: "a", href: "/signup" }}
            size="medium"
            color="blue"
            style={{ kind: "primary" }}
            label={$_("index.hero-button")}
        />
    </section>
</main>
