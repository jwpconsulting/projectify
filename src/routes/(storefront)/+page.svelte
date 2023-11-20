<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<HeroLayout heroBackground={false}>
    <div
        slot="hero"
        class="grid grid-cols-1 items-center gap-4 sm:grid-cols-2"
    >
        <div class="flex flex-col gap-12">
            <header class="flex flex-col gap-10">
                <h1 class="text-4xl font-bold md:text-6xl">
                    {$_("index.hero-header")}
                </h1>
                <p class="max-w-md">
                    {$_("index.hero-text")}
                </p>
            </header>
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                action={{ kind: "a", href: "/user/sign-up" }}
                label={$_("index.hero-button")}
                grow={false}
            />
        </div>
        <div class="min-w-full max-w-md">
            <img src="/assets/landing/hero.png" alt={$_("index.hero-alt")} />
        </div>
    </div>
    <div slot="content" class="flex flex-col gap-16">
        <div class="grid grid-cols-1 text-center sm:ml-32 sm:mr-32">
            <h2 class="mb-4 text-3xl font-bold md:text-5xl">
                {$_("index.trust-header-1")}
                <span class="text-primary">{$_("index.trust-header-2")}</span>
                {$_("index.trust-header-3")}
                <span class="text-primary">{$_("index.trust-header-4")}</span>
            </h2>
            <h4 class="text-2xl font-bold md:text-3xl">
                {$_("index.trust-text")}
            </h4>
        </div>
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-1.header"),
                text: $_("index.features.feature-1.text"),
                image: {
                    src: "/assets/landing/task-menu.png",
                    alt: $_("index.features.feature-1.alt"),
                    position: "right",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-2.header"),
                text: $_("index.features.feature-2.text"),
                image: {
                    src: "/assets/landing/sub-task.png",
                    alt: $_("index.features.feature-2.alt"),
                    position: "left",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-3.header"),
                text: $_("index.features.feature-3.text"),
                image: {
                    src: "/assets/landing/filters.png",
                    alt: $_("index.features.feature-3.alt"),
                    position: "right",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-4.header"),
                text: $_("index.features.feature-4.text"),
                image: {
                    src: "/assets/landing/notifications.png",
                    alt: $_("index.features.feature-4.alt"),
                    position: "left",
                },
            }}
        />

        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-5.header"),
                text: $_("index.features.feature-5.text"),
                image: {
                    src: "/assets/landing/responsive.png",
                    alt: $_("index.features.feature-5.alt"),
                    position: "right",
                },
            }}
        />
        <div class="page bg base-200 mt-8 p-6">
            <div class="mb-12 text-center">
                <h2 class="mb-4 text-2xl font-bold sm:text-4xl">
                    {$_("index.solution-header")}
                </h2>
                <p class="text-l">
                    {$_("index.solution-subtitle")}
                </p>
            </div>
            <div
                class="mb-8 grid grid-cols-1 gap-8 text-center text-xl font-bold underline sm:grid-cols-3 sm:text-3xl"
            >
                <div>
                    <img
                        src="assets/solutions/hero-development.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href={"solutions/development-teams"} class="mt-4">
                        {$_("index.solution-1")}
                    </a>
                </div>
                <div>
                    <img
                        src="assets/solutions/hero-research.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href="solutions/research">
                        {$_("index.solution-2")}
                    </a>
                </div>
                <div>
                    <img
                        src="assets/solutions/hero-project-management.png"
                        alt=""
                        class="mb-4"
                    />
                    <a href="solutions/project-management">
                        {$_("index.solution-3")}
                    </a>
                </div>
            </div>
            <div class="text-l text-center font-bold underline sm:text-xl">
                <a href="/">
                    {$_("index.solution-more")}
                </a>
            </div>
        </div>
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-6.header"),
                text: $_("index.features.feature-6.text"),
                image: {
                    src: "/assets/landing/privacy.png",
                    alt: $_("index.features.feature-6.alt"),
                    position: "right",
                },
            }}
        />
        <SolutionsFeature
            feature={{
                title: $_("index.features.feature-7.header"),
                text: $_("index.features.feature-7.text"),
                image: {
                    src: "/assets/landing/open-source.png",
                    alt: $_("index.features.feature-7.alt"),
                    position: "left",
                },
            }}
        />
    </div>
</HeroLayout>
