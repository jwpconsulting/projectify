<script lang="ts">
    import { fc } from "$lib/storybook";

    import ConfirmPasswordReset from "$lib/figma/screens/auth/ConfirmPasswordReset.svelte";
    import LogIn from "$lib/figma/screens/auth/LogIn.svelte";
    import RequestPasswordReset from "$lib/figma/screens/auth/RequestPasswordReset.svelte";
    import SignUp from "$lib/figma/screens/auth/SignUp.svelte";
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
