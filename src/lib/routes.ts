type routeItem = {
    label: string;
    to?: string;
    authRequired?: boolean; // When is true user is fetched
    forceNavigation?: boolean; // Force visibility in the nav bar even if auth is required
    fetchUser?: boolean;
    action?: (arg0: unknown) => void;
};

export default [
    {
        to: "/",
        label: "Home",
        authRequired: false,
        forceNavigation: false,
        fetchUser: true,
    },
    { label: "signup", to: "/signup", authRequired: false },
    { label: "signin", to: "/signin", authRequired: false },
    {
        label: "dashboard.dashboard",
        to: "/dashboard",
        authRequired: true,
        forceNavigation: true,
    },
    {
        label: "Profile",
        to: "/user/profile",
        authRequired: true,
        forceNavigation: false,
    },
] as routeItem[];
