// This will prevent svelte-kit from complaining about us calling
// fetch from within a load() fn. Even though we do retrieve the current
// workspace using the svelte kit provided fetch, in the page itself
// we subscribe to archived workspace boards, which in turn will fire off
// another fetch request -- this time using window.fetch. Since svelte kit
// will attempt to render this page in the server too, we have to be extra
// sure that it won't attempt it. Hence this line here:
export const ssr = false;
