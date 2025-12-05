---
title: Frontend page titles
---

This document shows the current page titles for the SvelteKit frontend pages.
I've extracted the titles by looking for the corresponding `<svelte:head>`
tag in each `+page.svelte` file. Example:

```html
<svelte:head>
    <title>{$_("accessibility.title")}</title>
</svelte:head>
```

Then, I looked up the corresponding title in the `frontend/src/messages/en.ts`
messages file.

| Route Path                                           | Page Title                                               |
| ---------------------------------------------------- | -------------------------------------------------------- |
| `/`                                                  | Projectify                                               |
| `accessibility/`                                     | Accessibility statement - Projectify                     |
| `contact-us/`                                        | Contact - Projectify                                     |
| `credits/`                                           | Credits and attribution - Projectify                     |
| `dashboard/`                                         | —                                                        |
| `dashboard/project/[uuid]/`                          | {title} - Projectify                                     |
| `dashboard/project/[uuid]/search/`                   | {title} - Projectify                                     |
| `dashboard/section/[uuid]/create-task/`              | Add task to {title} - Projectify                         |
| `dashboard/task/[uuid]/`                             | —                                                        |
| `dashboard/task/[uuid]/update/`                      | Editing task - Projectify                                |
| `dashboard/workspace/[uuid]/archive/`                | Project archive                                          |
| `dashboard/workspace/[uuid]/settings/`               | {title} settings - Projectify                            |
| `dashboard/workspace/[uuid]/settings/billing/`       | {title} billing - Projectify                             |
| `dashboard/workspace/[uuid]/settings/quota/`         | {title} quota - Projectify                               |
| `dashboard/workspace/[uuid]/settings/team-members/`  | {title} team members - Projectify                        |
| `download/`                                          | Download and install - Projectify                        |
| `ethicalads/`                                        | Projectify                                               |
| `free-software/`                                     | Free software - Projectify                               |
| `help/`                                              | Help - Projectify                                        |
| `help/basics/`                                       | Basics                                                   |
| `help/billing/`                                      | Billing                                                  |
| `help/filters/`                                      | Filters                                                  |
| `help/keyboard-shortcuts/`                           | Keyboard shortcuts                                       |
| `help/labels/`                                       | Labels                                                   |
| `help/projects/`                                     | Projects                                                 |
| `help/quota/`                                        | Workspace quotas                                         |
| `help/roles/`                                        | Roles                                                    |
| `help/sections/`                                     | Sections                                                 |
| `help/tasks/`                                        | Tasks                                                    |
| `help/team-members/`                                 | Team members                                             |
| `help/trial/`                                        | Trial workspace                                          |
| `help/workspaces/`                                   | Workspaces                                               |
| `onboarding/about-you/`                              | About you - Projectify                                   |
| `onboarding/assign-task/[uuid]/`                     | Task "{taskTitle}" has been assigned to you - Projectify |
| `onboarding/new-label/[uuid]/`                       | Create a label for "{taskTitle}" - Projectify            |
| `onboarding/new-project/[uuid]/`                     | Add your first project - Projectify                      |
| `onboarding/new-task/[uuid]/`                        | Create your first task - Projectify                      |
| `onboarding/new-workspace/`                          | Create a new workspace - Projectify                      |
| `onboarding/welcome/`                                | Onboarding - Projectify                                  |
| `pricing/`                                           | Pricing - Projectify                                     |
| `privacy/`                                           | Privacy policy - Projectify                              |
| `security/disclose/`                                 | Vulnerability Disclosure Policy                          |
| `security/general/`                                  | Security Information                                     |
| `solutions/`                                         | Solutions - Projectify                                   |
| `solutions/academic/`                                | Academic solutions                                       |
| `solutions/development-teams/`                       | Development solutions                                    |
| `solutions/personal-use/`                            | Personal solutions                                       |
| `solutions/project-management/`                      | Project management solutions                             |
| `solutions/remote-work/`                             | Remote solutions                                         |
| `solutions/research/`                                | Research solutions                                       |
| `tos/`                                               | Terms of service - Projectify                            |
| `user/confirm-email/[email]/[token]/`                | Email address confirmed                                  |
| `user/confirm-password-reset/[email]/[token]/`       | Reset your password - Projectify                         |
| `user/log-in/`                                       | Log in - Projectify                                      |
| `user/log-out/`                                      | Log out - Projectify                                     |
| `user/profile/`                                      | Other settings                                           |
| `user/profile/change-password/`                      | Change password                                          |
| `user/profile/changed-password/`                     | Password changed                                         |
| `user/profile/update-email-address/`                 | Update email address                                     |
| `user/profile/update-email-address/confirm/[token]/` | Confirming new email address                             |
| `user/profile/update-email-address/confirmed/`       | Email address updated successfully                       |
| `user/profile/update-email-address/requested/`       | Email address update requested                           |
| `user/request-password-reset/`                       | Reset your password - Projectify                         |
| `user/requested-password-reset/`                     | Password reset requested - Projectify                    |
| `user/reset-password/`                               | Password reset complete - Projectify                     |
| `user/sent-email-confirmation-link/`                 | —                                                        |
| `user/sign-up/`                                      | Sign up - Projectify                                     |
