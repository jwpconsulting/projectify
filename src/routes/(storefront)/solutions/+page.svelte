<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    interface Solution {
        href: string;
        title: string;
        image: {
            src: string;
            alt: string;
        };
        description: string;
    }

    let solutions: Solution[];
    $: solutions = [
        {
            href: "/solutions/development-teams",
            title: $_("solutions-page.developer"),
            image: {
                src: "assets/solutions/hero-development.png",
                alt: "TODO",
            },
            description: $_("solutions-page.dev-description"),
        },
        {
            href: "/solutions/research",
            title: $_("solutions-page.research"),
            image: {
                src: "assets/solutions/hero-research.png",
                alt: "TODO",
            },
            description: $_("solutions-page.research-description"),
        },
        {
            href: "/solutions/project-management",
            title: $_("solutions-page.project-management"),
            image: {
                src: "assets/solutions/hero-project-management.png",
                alt: "TODO",
            },
            description: $_("solutions-page.project-description"),
        },
        {
            href: "/solutions/academic",
            title: $_("solutions-page.academic"),
            image: {
                src: "assets/solutions/hero-academic.png",
                alt: "TODO",
            },
            description: $_("solutions-page.academic-description"),
        },
        {
            href: "/solutions/remote",
            title: $_("solutions-page.remote"),
            image: {
                src: "assets/solutions/hero-remote.png",
                alt: "TODO",
            },
            description: $_("solutions-page.remote-description"),
        },
        {
            href: "/solutions/personal-use",
            title: $_("solutions-page.personal-use"),
            image: {
                src: "assets/solutions/hero-personal.png",
                alt: "TODO",
            },
            description: $_("solutions-page.personal-description"),
        },
    ];
</script>

<div class="flex flex-col gap-20 pb-20">
    <div class="flex flex-col items-center bg-background p-6">
        <div
            class="flex max-w-4xl flex-col items-center gap-6 p-4 sm:grid sm:grid-cols-2 sm:p-20"
        >
            <div class="flex flex-col gap-6">
                <h1 class="text-4xl font-bold md:text-6xl">
                    {$_("solutions-page.hero-header")}
                </h1>
                <p class="max-w-md">
                    {$_("solutions-page.hero-text")}
                </p>
            </div>
            <div class="w-full max-w-xs">
                <img src="/assets/solutions/solution-hero.png" alt="TODO" />
            </div>
        </div>
    </div>
    <div class="grid grid-cols-1 gap-12 px-10 sm:grid-cols-3 sm:gap-8">
        {#each solutions as solution}
            <div class="flex flex-col gap-4">
                <a href={solution.href}>
                    <img
                        src={solution.image.src}
                        alt={solution.image.alt}
                        class="rounded-lg"
                    />
                </a>
                <div class="flex flex-col gap-4">
                    <p class="font-bold">
                        {solution.title}
                    </p>
                    <p class="font-normal">
                        {$_("solutions-page.dev-description")}
                    </p>
                    <Anchor
                        size="normal"
                        href={solution.href}
                        label={$_("solutions-page.more")}
                    />
                </div>
            </div>
        {/each}
    </div>
</div>
