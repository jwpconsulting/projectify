<script>
    import HeaderLogo from "../assets/headerLogo.svelte";
    import Header from "../Header.svelte";

    export let footerVisible = true;
</script>

<Header />
<slot />
{#if footerVisible}
    <footer class="flex justify-center border-t border-base-300">
        <div
            class="flex items-center justify-start w-full max-w-3xl py-8 px-4"
        >
            <HeaderLogo />
        </div>
    </footer>
{/if}
