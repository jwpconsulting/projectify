<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <section class="relative">
            <div
                class="bg-debug absolute top-[-80px] right-0 h-[500px] w-[55%] max-w-4xl overflow-hidden rounded-bl-3xl"
            >
                <img
                    class="object-left-center h-full w-full object-cover"
                    src="/assets/landing/hero.jpg"
                    alt=""
                />
            </div>
            <div class="container relative grow">
                <div class="flex max-w-md flex-col gap-4 bg-base-100 p-6">
                    <h1 class="text-5xl">
                        Fast and easy-to-use project management tool
                    </h1>
                    <ul class="flex flex-col gap-2">
                        {#each ["Simple design that even beginners can use", "Easy to organize tasks to do now", "Easy to grasp the entire project at a glance", "100% open source software"] as item}
                            <div class="flex items-center gap-2">
                                <div>
                                    <svg
                                        width="20"
                                        height="20"
                                        viewBox="0 0 20 20"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                    >
                                        <rect
                                            x="0.5"
                                            y="0.5"
                                            width="19"
                                            height="19"
                                            rx="5.5"
                                            fill="#76B4F9"
                                            stroke="#76B4F9"
                                        />
                                        <path
                                            d="M5.78222 9.24833C5.39131 8.85819 4.75814 8.85881 4.368 9.24972C3.97786 9.64063 3.97849 10.2738 4.36939 10.6639L5.78222 9.24833ZM8.45964 13.3333L7.75323 14.0411L8.45504 14.7416L9.16141 14.0457L8.45964 13.3333ZM15.9291 7.37906C16.3225 6.99148 16.3273 6.35834 15.9397 5.96489C15.5521 5.57144 14.919 5.56668 14.5255 5.95425L15.9291 7.37906ZM4.36939 10.6639L7.75323 14.0411L9.16606 12.6255L5.78222 9.24833L4.36939 10.6639ZM9.16141 14.0457L15.9291 7.37906L14.5255 5.95425L7.75787 12.6209L9.16141 14.0457Z"
                                            fill="white"
                                        />
                                    </svg>
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
    </main>
</PageLayout>

<style lang="scss">
    section {
        @apply min-h-16 flex justify-center;
        @apply bg-base-100;

        > .container {
            // @apply bg-primary;
            // max-width: 1200px;
            @apply flex;
        }
    }
</style>
