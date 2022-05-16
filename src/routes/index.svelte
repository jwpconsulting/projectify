<script lang="ts">
    import BgLogo from "$lib/components/assets/landing/bg-logo.svelte";
    import IconCheck from "$lib/components/assets/landing/icon-check.svelte";
    import IllComA from "$lib/components/assets/landing/ill-com-A.svelte";
    import IllComB from "$lib/components/assets/landing/ill-com-B.svelte";
    import IllComC from "$lib/components/assets/landing/ill-com-C.svelte";
    import IllGithub from "$lib/components/assets/landing/ill-github.svelte";
    import IllSolution from "$lib/components/assets/landing/ill-solution.svelte";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";

    const heroList = [
        "Simple design that even beginners can use",
        "Easy to organize tasks to do now",
        "Easy to grasp the entire project at a glance",
        "100% open source software",
    ];

    const commobProblems = [
        {
            illustration: IllComA,
            title: "I can’t concentrate on important work.",
            body: "My job begins with finding the information I need by email or chat. If I have many tasks, I may not know which one is the most important.",
        },
        {
            illustration: IllComB,
            title: "The tools I'm currently using are complicated and difficult to use.",
            body: "I am not satisfied with the operability of the current tool. Task sharing is inefficient and difficult to manage.",
        },
        {
            illustration: IllComC,
            title: "I don't know if the team is moving towards the goal.",
            body: "I don't even know if the project is going well because I don't know the whole situation.",
        },
    ];

    const solutions = [
        "UI that makes it easy to see the entire task",
        "Easy to organize tasks to do now",
        "Easily organize what you need to do in the future",
    ];
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <!-- Section: Hero -->
        <section class="relative">
            <div
                class="bg-debug absolute right-0 w-full max-w-4xl overflow-hidden md:top-[0px] md:h-[500px] md:w-[55%] md:rounded-bl-3xl"
            >
                <img
                    class="md:object-left-center h-full w-full object-cover object-bottom"
                    src="/assets/landing/hero.jpg"
                    alt=""
                />
            </div>
            <div class="container relative min-h-[440px] pt-[70vw] md:pt-0">
                <div
                    class="m-6 flex flex-col gap-4 bg-base-100 p-6 md:m-0 md:max-w-md"
                >
                    <h1 class="text-4xl font-bold md:text-5xl">
                        Fast and easy-to-use project management tool
                    </h1>
                    <ul class="flex flex-col gap-2">
                        {#each heroList as item}
                            <div class="flex items-center gap-2">
                                <div>
                                    <IconCheck />
                                </div>
                                {item}
                            </div>
                        {/each}
                        <li />
                    </ul>
                    <button class="btn-action btn max-w-fit"
                        >Ger started</button
                    >
                </div>
            </div>
        </section>

        <!-- Section: Common Problems -->
        <section class="px-6 pb-20 md:py-20">
            <div class="section-anchor" id="problem" />
            <div
                class="container flex flex-col items-center justify-center gap-4"
            >
                <h1
                    class="text-center text-[2rem] font-bold leading-[1.2em] sm:text-[3.2rem]"
                >
                    Common Problem
                </h1>
                <h2
                    class="-mb-10 text-center text-[1rem] leading-[1.2em] sm:text-2xl"
                >
                    Various problems occur when working.
                </h2>
                <div
                    class="grid w-full grid-cols-1 gap-6 gap-y-0  md:grid-cols-3"
                >
                    {#each commobProblems as item}
                        <div
                            class="mt-28 flex flex-col gap-4 rounded-2xl bg-neutral p-8 text-neutral-content dark:bg-base-300"
                        >
                            <div
                                class="-mt-20 flex items-center justify-center md:min-h-[180px]"
                            >
                                <svelte:component this={item.illustration} />
                            </div>
                            <h1 class="text-2xl font-bold">{item.title}</h1>
                            <div class="text-lg font-light">{item.body}</div>
                        </div>
                    {/each}
                </div>
            </div>
        </section>

        <!-- Section: Solution  -->
        <section class="solution relative px-6 pt-20">
            <div class="section-anchor" id="solution" />
            <div class="absolute left-8 top-0 h-full overflow-hidden">
                <BgLogo />
            </div>
            <div class="absolute top-0 left-[50%] flex h-1 w-1 justify-center">
                <div
                    class="h-20 w-20 shrink-0 translate-y-[-50%] rotate-45 rounded-br-3xl bg-base-100"
                />
            </div>
            <div
                class="container z-[1] flex flex-col items-center justify-center gap-4 text-primary-content"
            >
                <h1
                    class="title-shadow text-center text-[2.0rem] font-bold leading-[1.2em] sm:text-[3.2rem]"
                >
                    Resolve By Projectify
                </h1>
                <h2
                    class="title-shadow text-center text-[1rem] leading-[1.2em] sm:text-2xl"
                >
                    A design that allows you to simply group tasks together and
                    share them quickly.
                </h2>
                <div class="-mb-8 w-full max-w-4xl">
                    <IllSolution />
                </div>
            </div>
        </section>
        <section class="flex bg-base-200 px-6 py-10 pt-20 md:py-20">
            <div class="container flex">
                <div
                    class="flex w-full flex-col  items-stretch gap-6 md:grid md:grid-cols-3"
                >
                    {#each solutions as text, inx}
                        <div
                            class="flex w-full items-start gap-4 rounded-2xl bg-base-100 p-4 text-2xl font-bold dark:bg-base-300"
                        >
                            <div
                                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary text-primary-content"
                            >
                                {inx + 1}
                            </div>
                            <span class="">{text}</span>
                        </div>
                    {/each}
                </div>
            </div>
        </section>

        <!-- Section Github -->
        <section class="relative min-h-[100vw] py-10 px-6 md:py-20">
            <div class="section-anchor" id="github" />
            <div
                class="container grid grid-cols-1 items-center justify-center overflow-hidden rounded-3xl shadow-2xl dark:bg-base-300 md:grid-cols-2"
            >
                <div
                    class="flex h-full w-full items-center justify-center bg-[#000] p-8 md:order-last"
                >
                    <div class="max-w-[200px]">
                        <IllGithub />
                    </div>
                </div>
                <div class="flex w-full flex-col gap-4 p-6 md:p-10">
                    <h1 class="text-2xl font-bold">
                        Projectify is 100% open source software
                    </h1>
                    <h2 class="text-md max-w-lg">
                        Currently 4 people are participating in the project.
                        Projectify has a more active development community.
                    </h2>
                    <a href="/" class="btn-action btn w-fit">Learn more</a>
                    <div>
                        Currently <span class="font-bold text-primary"
                            >1,140</span
                        > people are participating
                    </div>
                </div>
            </div>
        </section>
    </main>
</PageLayout>

<style lang="scss">
    section {
        @apply min-h-16 relative flex justify-center;
        &.solution {
            background: linear-gradient(
                -45deg,
                hsla(var(--p) / 30%),
                hsla(var(--p) / 60%)
            );
        }

        > .section-anchor {
            z-index: 2000;
            @apply absolute -top-20 left-0;

            @media screen and (max-width: 425px) {
                &#problem {
                    opacity: 0.3;
                    top: -128px !important;
                }
            }
        }

        .title-shadow {
            text-shadow: 0px 1px 2px rgba(#000, 0.3);
        }
    }
</style>
