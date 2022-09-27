<script lang="ts">
    import LogIn from "$lib/figma/LogIn.svelte";
    import SignUp from "$lib/figma/SignUp.svelte";
    import RequestPasswordReset from "$lib/figma/RequestPasswordReset.svelte";
    import ConfirmPasswordReset from "$lib/figma/ConfirmPasswordReset.svelte";

    import { fc } from "$lib/storybook";
</script>

<div class={fc}>
    <div class="w-[500px]">
        <LogIn />
    </div>
    <div class="w-[500px]">
        <SignUp />
    </div>
    <div class="w-[500px]">
        <RequestPasswordReset />
    </div>
    <div class="w-[500px]">
        <ConfirmPasswordReset
            email="hello@example.com"
            token="asdhelloworld"
        />
    </div>
</div>
