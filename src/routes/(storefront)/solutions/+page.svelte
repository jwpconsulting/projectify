<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    import HeroAcademic from "./assets/hero-academic.png";
    import HeroDevelopmentTeams from "./assets/hero-development-teams.png";
    import HeroPersonal from "./assets/hero-personal.png";
    import HeroProjectManagement from "./assets/hero-project-management.png";
    import HeroRemoteWork from "./assets/hero-remote-work.png";
    import HeroResearch from "./assets/hero-research.png";
    import HeroSolutions from "./assets/hero-solutions.png";

    interface Solution {
        href: string;
        title: string;
        image: {
            src: string;
            alt: string;
        };
        description: string;
    }

    $: heroContent = {
        title: $_("solutions.index.hero.title"),
        text: $_("solutions.index.hero.text"),
        image: {
            src: HeroSolutions,
            alt: $_("solutions.index.hero.illustration.alt"),
        },
    } satisfies SolutionsHeroContent;

    $: solutions = [
        {
            href: "/solutions/development-teams",
            title: $_("solutions.index.solutions.development.title"),
            image: {
                src: HeroDevelopmentTeams,
                alt: $_(
                    "solutions.index.solutions.development.illustration.alt",
                ),
            },
            description: $_(
                "solutions.index.solutions.development.description",
            ),
        },
        {
            href: "/solutions/research",
            title: $_("solutions.index.solutions.research.title"),
            image: {
                src: HeroResearch,
                alt: $_("solutions.index.solutions.research.illustration.alt"),
            },
            description: $_("solutions.index.solutions.research.description"),
        },
        {
            href: "/solutions/project-management",
            title: $_("solutions.index.solutions.project-management.title"),
            image: {
                src: HeroProjectManagement,
                alt: $_(
                    "solutions.index.solutions.project-management.illustration.alt",
                ),
            },
            description: $_(
                "solutions.index.solutions.project-management.description",
            ),
        },
        {
            href: "/solutions/academic",
            title: $_("solutions.index.solutions.academic.title"),
            image: {
                src: HeroAcademic,
                alt: $_("solutions.index.solutions.academic.illustration.alt"),
            },
            description: $_("solutions.index.solutions.academic.description"),
        },
        {
            href: "/solutions/remote-work",
            title: $_("solutions.index.solutions.remote-work.title"),
            image: {
                src: HeroRemoteWork,
                alt: $_(
                    "solutions.index.solutions.remote-work.illustration.alt",
                ),
            },
            description: $_(
                "solutions.index.solutions.remote-work.description",
            ),
        },
        {
            href: "/solutions/personal-use",
            title: $_("solutions.index.solutions.personal-use.title"),
            image: {
                src: HeroPersonal,
                alt: $_(
                    "solutions.index.solutions.personal-use.illustration.alt",
                ),
            },
            description: $_(
                "solutions.index.solutions.personal-use.description",
            ),
        },
    ] satisfies Solution[];
</script>

<HeroLayout>
    <Hero slot="hero" {heroContent} />
    <div
        slot="content"
        class="flex flex-col items-center gap-12 md:grid md:grid-cols-3 md:gap-8"
    >
        {#each solutions as solution}
            <section class="flex h-full flex-col justify-between gap-4">
                <div class="flex flex-col gap-4">
                    <img
                        src={solution.image.src}
                        alt={solution.image.alt}
                        class="rounded-lg"
                    />
                    <div class="flex h-full flex-col gap-4">
                        <h2 class="font-bold">
                            {solution.title}
                        </h2>
                        <p class="font-normal">
                            {solution.description}
                        </p>
                    </div>
                </div>
                <Anchor
                    size="normal"
                    href={solution.href}
                    label={$_("solutions.index.more")}
                />
            </section>
        {/each}
    </div>
</HeroLayout>
