type routeItem = {
    label: string;
    to?: string;
    authRequired?: boolean;
    forceNavigation?: boolean;
    fetchUser?: boolean;
    action?: (any) => void;
};

export default [
    { label: "home", to: "/" },
    { label: "signup", to: "/signup", authRequired: false },
    { label: "signin", to: "/signin", authRequired: false },
    {
        label: "dashboard",
        to: "/dashboard",
        authRequired: true, // When is true user is fetched
        forceNavigation: true, // Force visibility in the nav bar even if auth is required
    },
] as routeItem[];
