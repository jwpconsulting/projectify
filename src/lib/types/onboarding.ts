export const onboardingStates = [
    "about-you",
    "new-workspace",
    "billing-details",
    "payment-success",
    "payment-error",
    "new-board",
    "new-task",
    "new-section",
    "new-label",
    "assign-task",
] as const;

export type OnboardingState = typeof onboardingStates[number];
