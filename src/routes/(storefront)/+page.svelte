<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
</script>

<HeroLayout heroBackground={false}>
    <section
        slot="hero"
        class="grid grid-cols-1 items-center gap-4 sm:grid-cols-2"
    >
        <div class="flex flex-col gap-12">
            <header class="flex flex-col gap-10">
                <h1 class="text-4xl font-bold md:text-6xl">
                    {$_("index.hero-header")}
                </h1>
                <p>
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
        <div class="max-w-md">
            <img src="/assets/landing/hero.png" alt={$_("index.hero-alt")} />
        </div>
    </section>
    <div slot="content" class="flex flex-col gap-16">
        <section class="flex flex-col gap-4">
            <h2 class="text-center text-3xl font-bold md:text-5xl">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("index.trust.header")}
            </h2>
            <h4 class="text-center text-2xl font-bold md:text-3xl">
                {$_("index.trust.text")}
            </h4>
        </section>
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
        <section class="flex flex-col gap-7">
            <header class="flex flex-col gap-3">
                <h2 class="text-2xl font-bold sm:text-4xl">
                    {$_("index.solution-header")}
                </h2>
                <p>
                    {$_("index.solution-subtitle")}
                </p>
            </header>
            <div class="flex flex-col gap-5 text-center">
                <div class="grid grid-cols-1 gap-8 sm:grid-cols-3">
                    <div class="flex flex-col gap-3">
                        <img
                            src="assets/solutions/hero-development.png"
                            alt=""
                        />
                        <Anchor
                            size="large"
                            href={"solutions/development-teams"}
                            label={$_("index.solution-1")}
                        />
                    </div>
                    <div class="flex flex-col gap-3">
                        <img src="assets/solutions/hero-research.png" alt="" />
                        <Anchor
                            size="large"
                            href={"solutions/research"}
                            label={$_("index.solution-2")}
                        />
                    </div>
                    <div class="flex flex-col gap-3">
                        <img
                            src="assets/solutions/hero-project-management.png"
                            alt=""
                        />
                        <Anchor
                            size="large"
                            href={"solutions/project-management"}
                            label={$_("index.solution-3")}
                        />
                    </div>
                </div>
                <Anchor
                    size="large"
                    href={"solutions/"}
                    label={$_("index.solution-more")}
                />
            </div>
        </section>
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
