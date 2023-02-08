<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
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
    $: cards = [
        {
            figure: $_("pricing-page.card-figure-1"),
            description: $_("pricing-page.card-description-1"),
        },
        {
            figure: $_("pricing-page.card-figure-2"),
            description: $_("pricing-page.card-description-2"),
        },
        {
            figure: $_("pricing-page.card-figure-3"),
            description: $_("pricing-page.card-description-3"),
        },
    ];
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <div class="mt-8 text-center">
            <h1 class="mb-4 text-4xl font-bold sm:text-6xl">
                {$_("pricing-page.header")}
            </h1>
            <h4 class="sm-text-3xl text-3xl font-bold">
                {$_("pricing-page.subtitle")}
            </h4>
        </div>
        <div>
            <div
                class="page bg base-200 m-4 grid grid-cols-1 gap-4 p-12 text-center sm:m-16 sm:grid-cols-3"
            >
                <div>
                    <h4 class="text-3xl font-bold">
                        {$_("pricing-page.plan")}
                    </h4>
                </div>
                <div class="flexbox flex justify-center gap-4">
                    <div>
                        <h2 class="text-5xl font-bold">
                            {$_("pricing-page.price")}
                        </h2>
                    </div>
                    <div>
                        <div>
                            {$_("pricing-page.seat")}
                        </div>
                        <div>
                            {$_("pricing-page.month")}
                        </div>
                    </div>
                </div>
                <div>
                    <a
                        href={"/signup"}
                        class="btn btn-primary btn-md max-w-fit"
                    >
                        {$_("index.hero-button")}
                    </a>
                </div>
            </div>
        </div>
        <div class="space-y-8 text-center text-2xl font-bold">
            <p>
                {$_("pricing-page.feature-title")}
            </p>
            <div class="flex justify-center text-xl">
                <ul class="">
                    {#each features as feature}
                        <li class="ml-10 flex flex-row items-center gap-4">
                            <div>
                                <Icon
                                    src={Check}
                                    theme="outline"
                                    class="h-4 w-4 text-base-content"
                                />
                            </div>
                            {feature}
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
        <div class="mt-16 text-center text-3xl font-bold">
            <h4>
                {$_("pricing-page.join")}
            </h4>
        </div>
        <div
            class="m-8 grid grid-cols-1 gap-8 text-center text-base-100 sm:m-16 sm:grid-cols-3"
        >
            {#each cards as card}
                <div class="page rounded-lg bg-base-content p-6">
                    <h2 class="text-5xl font-bold">
                        {card.figure}
                    </h2>
                    <p>
                        {card.description}
                    </p>
                </div>
            {/each}
        </div>
    </main>
</PageLayout>

<style lang="scss">
</style>
