type routeItem = {
    label: string;
    to?: string;
    authRequired?: boolean;
    forceNavigation?: boolean;
    action?: (any) => void;
};

export default [
    { label: "Home", to: "/" },
    { label: "Signup", to: "/signup", authRequired: false },
    {
        label: "Tasks",
        to: "/tasks",
        authRequired: true, // When is true user is fetched
        forceNavigation: true, // Force visibility in the nav bar even if auth is required
    },
];
