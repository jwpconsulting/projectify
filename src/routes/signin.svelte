<script lang="ts">
    import { client } from "$lib/graphql-client";
</script>

<main class="page page-center">
    <div class="panel">
        <div class="field">
            <div class="label">Email</div>
            <input type="email" placeholder="email" />
        </div>
        <div class="field">
            <div class="label">Password</div>
            <input type="password" placeholder="password" />
        </div>
        <button class="btn-primary">Sign in</button>
    </div>
</main>
