<script lang="ts">
    import { client } from "$lib/graphql-client";

    let usernameValue;
    let passwordValue;

    function submit() {}
</script>

<main class="page page-center">
    <div class="card text-center shadow-card">
        <div class="card-body items-center">
            <div class="py-2">
                <h1 class="card-title">Sign in</h1>
                <div>
                    Let’s set up your account, Don't have one yet?<wbr />
                    <a class="link link-primary" href="/singup">
                        Sign up here.
                    </a>
                </div>
            </div>

            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">Username</span>
                </label>
                <input
                    type="text"
                    placeholder="username"
                    class="input input-bordered"
                />
            </div>

            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">Password</span>
                </label>
                <input
                    type="password"
                    placeholder="password"
                    class="input input-bordered"
                />
            </div>
            <div class="p-2 text-error">Wrong username or password.</div>

            <div class="pt-7">
                <button class="btn btn-primary">Sign in</button>

                <div class="p-2">
                    Forget password? Password reset
                    <a class="link link-primary" href="/reset">here.</a>
                </div>
            </div>
        </div>
    </div>
</main>
