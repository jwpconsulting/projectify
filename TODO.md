# Features

-   Remember with sidenav menus have been open and not in localstorage

# Unfinished

-   Reintegrate mobile menu overlay as proper overlay (whatever that means)

# Bug

-   Solve issue where all headers have different heights (at least on Desktop)
-   Fix issue where buttons don't react well when placed inside an items-center
    flex with column layout
-   dashboard/task/uuid does not support refetching (Still a bug? Justus 2023-05-01)
-   Add new workspace board section overlay does not react well when pressing
    enter. Justus 2023-05-01
-   In the task card on the dashboard, the sub task progress is falsely shown as
    100 % for tasks with no sub tasks. Justus 2023-05-01
-   Clicking cancel doesn't do anything in the constructive overlays
-   It would be nice to show login after attempting to fetch user

# Refactor

-   Tertiary nav btns to be replaced by HeaderButton
-   Update button to use ButtonAction
-   All overlays should use async functions so we can await them finishing /
    closing / whatever it is that they do
-   Make undefined and null for empty form fields more consistent
-   Factor disabled state into ButtonAction (since anchors cannot be disabled)

# Update Dependency

-   Update @steeze-ui/heroicons. Some of the icons have been renamed (search, eye, ...)

# QA

-   Consider introducing shellcheck
-   Warn about unused variables (possible just in svelte files)

# DONE

-   The drop down in user assignment does not indicate the current assignee
