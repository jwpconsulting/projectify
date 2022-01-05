import { writable } from 'svelte/store';
import { goto } from "$app/navigation";

export const user = writable(null);
export const singinRedirect = { to: null };

user.subscribe(u => {
  if (u) {
    if (singinRedirect.to == null) {
      goto("/");
    } else {
      goto(singinRedirect.to);
      singinRedirect.to = null;
    }
  }
})
