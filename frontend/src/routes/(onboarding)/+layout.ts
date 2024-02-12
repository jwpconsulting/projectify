import { load } from "../(platform)/+layout";

// We re-export load from platform to have same functionality without
// duplication
export { load };

// Perhaps something in this hierarchy can be prerendered?
// TODO check
export const prerender = false;
// SSR, this can be prerendered
export const ssr = false;
