// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { MessageDirectory } from "./types";

const messages: MessageDirectory = {
    "overlay": {
        "constructive": {
            "update-workspace-board": {
                title: "Edit workspace board",
                form: {
                    title: {
                        label: "workspace board name",
                        placeholder: "Enter a workspace board name",
                    },
                },
                cancel: "Cancel",
                save: "Save",
            },
            "create-workspace-board": {
                "title": "Create workspace board",
                "form": {
                    title: {
                        label: "Workspace board name",
                        placeholder: "Enter a workspace board name",
                    },
                },
                "cancel": "Cancel",
                "create-board": "Create",
            },
            "invite-workspace-user": {
                title: "Invite workspace user",
                form: {
                    email: {
                        label: "Enter the email address of the user you would like to invite",
                        placeholder: "workspace-user@mail.com",
                        validation: {
                            ok: "The user was successfully invited",
                        },
                    },
                },
                cancel: "Cancel",
                invite: "Invite",
            },
            "create-workspace-board-section": {
                "title": "Create new workspace board section",
                "form": {
                    title: {
                        label: "New workspace board section name",
                        placeholder: "New workspace board section name",
                    },
                },
                "cancel": "Cancel",
                "create-section": "Create",
            },
            "update-workspace-board-section": {
                title: "Edit workspace board section",
                form: {
                    title: {
                        label: "Workspace board section title",
                        placeholder: "Enter new workspace board section title",
                    },
                },
                cancel: "Cancel",
                update: "Save",
            },
            "recover-workspace-board": {
                "title": "Recover this board?",
                "notice": "Recovering this board returns it to the dashboard",
                "cancel": "Cancel",
                "recover-board": "Recover board",
            },
        },
        "destructive": {
            "delete-label": {
                title: "Delete label",
                body: "Would you like to delete the ''{label}'' label?",
                button: "Delete",
                warning: "This action cannot be undone.",
            },
            "delete-workspace-user": {
                title: "Remove workspace user",
                body: "Would you like to remove ''{workspaceUser}'' from this workspace?",
                warning: "This action cannot be undone.",
                button: "Remove",
            },
            "delete-workspace-board-section": {
                title: "Delete workspace board section",
                body: "Would you like to delete the ''{workspaceBoardSection}'' workspace board section?",
                warning:
                    "Deleting this section will also delete all tasks within it.",
                button: "Delete",
            },
            "delete-task": {
                title: "Delete task",
                body: "Would you like to delete the ''{task}'' task?",
                warning: "This action cannot be undone.",
                button: "Delete",
            },
            "delete-selected-tasks": {
                title: "Delete selected tasks",
                body: "Would you like to delete {count, number} selected tasks?",
                warning: "This action cannot be undone.",
                button: "Delete",
            },
            "archive-workspace-board": {
                title: "Archive workspace board",
                body: "Would you like to archive this ''{workspaceBoard}'' workspace board?",
                warning:
                    "You can see archived workspace boards in the archives section",
                button: "Archive",
            },
            "delete-workspace-board": {
                title: "Delete workspace board",
                body: "Would you like to delete this ''{workspaceBoard}'' workspace board?",
                warning: "This action cannot be undone",
                button: "Delete",
            },
            "cancel": "Cancel",
        },
        "context-menu": {
            "profile": {
                "my-profile": "My profile",
                "log-out": "Log out",
            },
            "workspace": {
                "select-workspace": "Switch to workspace:",
            },
            "side-nav": {
                "minimise-sidebar": "Minimise sidebar",
                "expand-sidebar": "Expand sidebar",
                "go-to-archive": "Go to archive",
                "workspace-settings": "Workspace settings",
            },
            "workspace-board": {
                "edit-board": "Edit board",
                "archive-workspace-board": "Archive board",
            },
            "workspace-board-section": {
                "expand-section": "Expand section",
                "collapse-section": "Collapse section",
                "switch-previous": "Switch with previous section",
                "switch-next": "Switch with next section",
                "edit-title": "Edit section title",
                "delete-workspace-board-section": "Delete section",
            },
            "task": {
                "open-task": "Open task",
                "move-to-section": "Move to section",
                "move-to-top": "Move to top",
                "move-to-bottom": "Move to bottom",
                "copy-link": "Copy link",
                "delete-task": "Delete task",
            },
            "help": {
                "help-and-tips": "Help and tips",
                "blog": "Blog",
            },
            "permissions": {
                "all-roles": "All roles",
                "owner": "Owner",
                "maintainer": "Maintainer",
                "member": "Member",
                "observer": "Observer",
            },
        },
    },
    // TODO find out if we can factor this into somewhere
    "label": {
        "apply-label": "Assign label",
    },
    "dashboard": {
        "actions": {
            "add-workspace-board-section": "Add workspace board section",
        },
        "task-card": {
            "add-label": "Assign label",
            "task-number": "#{number}",
        },
        "search": {
            "not-found": {
                title: "No tasks found for ''{search}''",
                explanation:
                    "No tasks were found for the search terms you specified. You can either try a new search using the search form above or go back and view entire the workspace board.",
                back: "Go back to workspace board",
            },
            "found": {
                title: "Showing results for ''{search}''",
                back: "Go back to workspace board",
            },
        },
        "create-board": "Create new workspace board",
        "boards": "Workspace boards",
        "workspace-users": "Workspace users",
        "workspace-user-name": "Workspace user name",
        "filter-workspace-users": "Filter workspace users",
        "search-task": {
            button: "Search tasks",
            input: { placeholder: "Enter search terms", label: "Task search" },
        },
        "assign-user": "Assign workspace user",
        "no-sections": {
            message: "There are no sections in this workspace board.",
            prompt: "Add a section",
        },
        "section": {
            "empty": {
                message: "No tasks in this section.",
                prompt: "Add a task here",
            },
            "add-task": "Add task",
        },
        "no-user-assigned": "No workspace user assigned",
        "error": {
            "title": "Error:",
            "description":
                "We apologize for the error. There was an error loading your dashboard. The error details are as follows:",
            "what-to-do": {
                message:
                    "Unfortunately this means we are unable to load this page properly. To help resolve this:",
                options: {
                    "help": "Visit the help page for common solutions",
                    "contact-us": "Contact us",
                },
            },
        },
        "side-nav": {
            "no-workspace": {
                title: "No workspace selected",
                message:
                    "To use a workspace, click the workspace selector above and select the workspace you would like to use.",
            },
            "workspace-selector": {
                "select": "Select a workspace",
                "context-menu": "Open workspace context menu",
            },
            "workspace-boards": {
                empty: {
                    message:
                        "You have no workspace boards available. Please check the workspace board archive and recover a workspace board from there. Alternatively you can also create a new workspace board using the button below.",
                    archive: "Go to archive",
                },
            },
            "filter-labels": {
                "title": "Filter labels",
                "create-new-label": "Create new label",
                "input": {
                    label: "Label name",
                    placeholder: "Filter by label name",
                },
                "create-input": {
                    label: "Label name",
                    placeholder: "New label name",
                },
                "color": {
                    prompt: "Select label color",
                    colors: {
                        orange: "Orange",
                        pink: "Pink",
                        blue: "Blue",
                        purple: "Purple",
                        yellow: "Yellow",
                        red: "Red",
                        green: "Green",
                    },
                },
                "update-input": {
                    label: "Label name",
                    placeholder: "New name for label",
                },
                "state": {
                    update: "Updating label {label}",
                    create: "New label",
                },
                "errors": {
                    create: "The label could not be created. Please make sure you entered a valid name and color and try again.",
                    update: "The label could not be updated. Please make sure you entered a valid name and color and try again.",
                },
                "save": "Save",
                "cancel": "Cancel",
            },
        },
    },
    "workspace-board-archive": {
        title: "Workspace board archive",
        card: {
            recover: "Recover",
            delete: "Delete",
            archived: "Archived on {archived, date, medium}",
        },
        empty: "No workspace boards have been archived.",
    },
    // Factor this into a general error section
    "page404": {
        title: "Lost your way?",
        body: "The page you're looking for doesn't exist.",
        home: "Take me home",
    },
    // Factor this into a general error section
    "connection-status": {
        "disconnected": "Not connected to Projectify",
        "back-to-landing": "Back to landing page",
    },
    // TODO factor this into "dashboard"?
    "filter-label": {
        all: "All labels",
        none: "No label",
    },
    // TODO factor this into "dashboard"?
    "filter-workspace-user": {
        "all-users": "All users",
        "assigned-nobody": "Assigned to nobody",
    },
    "onboarding": {
        "continue": "Continue",
        "back": "Back",
        "welcome": {
            title: "Welcome",
            prompt: [
                "In the following steps you will create a new workspace and create your first task.",
                "You can use the workspace in trial mode at the beginning, and upgrade to a paid version anytime by going to the workspace settings.",
            ],
            help: {
                "trial-mode-features":
                    "Learn more about features available during trial mode",
            },
        },
        "about-you": {
            title: "About you",
            input: {
                label: "Preferred name (optional)",
                placeholder: "Your preferred name",
            },
            prompt: "Tell us your preferred name. You can also keep it empty and continue by clicking the button below.",
            greeting: {
                "with-name": "Welcome, {name}! 👋",
                "without-name": "Welcome! 👋",
            },
        },
        "new-workspace": {
            "title": {
                "with-name": "Let’s set up your first workspace, {who}.",
                "without-name": "Let's set up your first workspace.",
            },
            "prompt": "You can create and manage numerous workspaces",
            "has-workspace":
                "It looks like you already have a workspace, would you like to create a workspace board?",
            "label": "Workspace name",
            "placeholder": "e.g. the name of your company",
            "default-name": "Your workspace",
        },
        "new-workspace-board": {
            "title": "Add your first board",
            "prompt": [
                "You can create unlimited boards per workspace.",
                "They help you to focus on different projects you may be working on.",
            ],
            "input": {
                label: "Board title",
                placeholder: "Release spring Aug 2023",
            },
            "default-name": "Your board",
            "workspace-board-exists": {
                message:
                    'It looks like you already have a workspace board called "{title}". Would you like to continue adding a task for it?',
                prompt: 'Continue adding task to "{title}"',
            },
        },
        "new-task": {
            "title": "What is a task you’d like to complete?",
            "workspace-board-section-title": "To do",
            "default-name": "Your task",
            "prompt": {
                location:
                    'This task will be placed in a section called "{workspaceBoardSectionTitle}"',
                exists: 'It looks like you already have a workspace board section called "{workspaceBoardSectionTitle}". We will now create a task  and place it into that workspace board section.',
                explanation:
                    "Tasks can be further divided into sub tasks and contain detailed descriptions.",
            },
            "input": {
                label: "Task name",
                placeholder: "E.g., 'Add user permission dropdown'",
            },
        },
        "new-label": {
            "title": 'Create a label for "{taskTitle}"',
            "prompt": "Labels help you to filter between the types of tasks.",
            "input": {
                placeholder: "e.g., Bug",
                label: "Label name",
            },
            "error":
                "Please check the label name you have specified one more time and try again.",
            "default-name": "Your label",
        },
        "assign-task": {
            "title": 'Task "{taskTitle}" has been assigned to you!',
            "continue": "Get started",
            "prompt": {
                "finished": "You’re all set!",
                "adding-workspace-users":
                    "If you wish to add new workspace users to your workspace, please go to the workspace settings menu next to your workspace name.",
            },
            "follow-up": {
                "billing-help": "Learn more about workspace billing settings",
                "go-to-billing-settings": "Go to workspace billing settings",
            },
        },
        "error": {
            "title": "Onboarding failed",
            "message":
                "The last onboarding step did not finish correctly. Please try the onboarding process more time by clicking the button below.",
            "error-detail": "Error message:",
            "try-again": "Continue onboarding",
        },
    },
    "auth": {
        "sign-up": {
            "title": "Sign up",
            "sub-title": "Sign up and start a free trial",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
                missing: "Must enter email",
            },
            "password": {
                label: "Password",
                placeholder: "Enter your password",
                missing: "Must enter password",
            },
            "tos": {
                label: 'I agree to the <a href="{tosUrl}">Terms of Service</a>',
                missing: "Must agree to Terms of Service",
            },
            "privacy-policy": {
                label: 'I agree to the <a href="{privacyPolicyUrl}">Privacy Policy</a>',
                missing: "Must agree to Privacy Policy",
            },
            "submit": {
                ready: "Sign up",
                submitting: "Signing you up",
            },
            "already-have-an-account": "Already have an account?",
            "generic-error":
                "We are unable to sign you up with these credentials. Please confirm whether you have not signed up with this email already.",
            "log-in-here": "Log in here",
        },
        "confirmation-link-sent": {
            "header": "Email confirmation link sent",
            "illustration-alt":
                "Happy bird mascot indicating that a email confirm email is on its way to you",
            "body": "Please go to your email and follow the instructions to activate your account",
            "back-to-homepage": "Back to homepage",
        },
        "logout": {
            "success": "You have been logged out",
            "log-back-in": "Log in again",
            "landing": "Go to landing",
        },
        "log-in": {
            "title": "Log in",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
                missing: "Must enter email",
            },
            "password": {
                label: "Password",
                placeholder: "Enter your password",
                missing: "Must enter password",
            },
            "forgot-password": "Forgot password",
            "log-in": "Log in",
            "no-account": "Don't have an account yet?",
            "invalid-credentials":
                "Invalid credentials. Please check email and password.",
            "sign-up-here": "Sign up here",
        },
        "request-password-reset": {
            "title": "Reset your password",
            "explanation":
                "Enter the email associated with your account and we'll send you a link to reset your password.",
            "email": {
                label: "Email",
                placeholder: "Enter your email",
            },
            "submit": {
                start: "Send password reset link",
                submitting: "Submitting form...",
            },
            "return-to-log-in": "Return to log in",
            "error": {
                generic:
                    "Something went wrong when requesting your password reset link. Please try again using this form, or contact support if you have any questions",
                validation:
                    "Please check the fields above again for errors and submit again",
            },
        },
        "requested-password-reset": {
            "title": "Password reset requested",
            "message":
                "You have requested for your password to be reset and will receive an email with password reset instructions soon. Please check your email inbox.",
            "troubleshooting":
                "If you do not receive any email, you can request a new password email to be sent by using the email. Please contact support if you have any questions.",
            "request-again": "Request password reset again",
        },
        "confirm-password-reset": {
            "title": "Reset your password",
            "password-1": {
                label: "New password",
                placeholder: "Enter new password",
                validation: {
                    "no-match":
                        "The password entered here must match the password entered under 'Confirm new password'",
                },
            },
            "password-2": {
                label: "Confirm new password",
                placeholder: "Confirm new password",
                validation: {
                    "no-match":
                        "The password entered here must match the password entered under 'New password'",
                },
            },
            "validation": {
                "no-match":
                    "The two passwords you have entered do not match. Please check one more time if you have entered the same password in both fields.",
            },
            "submit": {
                start: "Reset password",
                submitting: "Resetting password...",
                error: "Reset password (try again)",
            },
            "error":
                "Your password could not be reset. Please try again. If you have previously reset your password using this form, please try requesting a password reset one more time using the link below.",
            "request-password-reset": "Request password reset again",
        },
        "reset-password": {
            title: "Password reset complete",
            message:
                "Your password was reset successfully. You may now proceed and log in with your email address and the password that you have just entered.",
            continue: "Continue to log in",
        },
        "confirm-email": {
            success: {
                title: "Email address confirmed",
                message:
                    "Your email address was confirmed successfully. You may now proceed to log in.",
                continue: "Continue to log in",
            },
            error: {
                title: "Error while confirming email address",
                message:
                    "Unfortunately your email address could not be confirmed. The error code from the API was:",
                continue: "Contact support",
            },
        },
    },
    "task-screen": {
        "update": {
            "update": "Update task",
            "update-continue-editing": "Update task and stay",
        },
        "create": {
            "create": "Create task",
            "create-continue-editing": "Create task and stay",
        },
        "sub-tasks": {
            "title": "Sub tasks",
            "completion": "{progress, number, percent} complete",
            "empty-state":
                "You have not added any sub tasks yet. You can add a sub task by clicking the add sub task button.",
            "empty-state-read-only":
                "This task has no sub tasks. You can add sub tasks by going to the task edit screen and clicking the add sub task button from there.",
            "add-sub-task": {
                button: "Add sub task",
            },
        },
        "new-task-breadcrumb": "New task (currently creating)",
        // TODO organize this as "form": {} with labels and placeholders
        "new-task-name": "New task name",
        "description": "Description",
        "labels": "Labels",
        "select-due-date": "Select due date",
        "due-date": "Due date",
        "edit": "Edit",
        "task-title": "Task title",
        "assignee": "Assignee",
        "enter-a-subtask": "Enter a subtask",
    },
    "user-account-settings": {
        "title": "User account settings",
        "overview": {
            "preferred-name": {
                label: "Preferred name (optional)",
                placeholder: "Enter your preferred name",
            },
            "profile-picture": {
                prompt: "Upload a profile picture",
                current: "Your current profile picture",
                remove: "Remove profile picture",
            },
            "update-email": "Update email address",
            "change-password": "Change password",
            "delete-account": "Delete account",
            "cancel": "Cancel",
            "save": "Save changes",
        },
        "update-email": {
            "title": "Change password",
            "current-password": {
                label: "Current password",
                placeholder: "Enter your current password",
            },
            "new-email": {
                label: "New email",
                placeholder: "Enter your new email address",
            },
            "cancel": "Go back",
            "save": "Update email",
        },
        "change-password": {
            "title": "Change password",
            "current-password": {
                label: "Current password",
                placeholder: "Enter your password",
            },
            "new-password": {
                label: "New password",
                placeholder: "Enter the new password",
            },
            "confirm-password": {
                label: "Confirm password",
                placeholder: "Confirm the new password",
            },
            "cancel": "Go back",
            "save": "Change password",
        },
    },
    "workspace-settings": {
        "title": "Workspace settings",
        "general": {
            "title": "General",
            "save": "Save",
            "cancel": "Cancel",
            "workspace-name": {
                label: "Workspace name",
                placeholder: "Enter a workspace name",
            },
            "description": {
                label: "Description",
                placeholder: "Enter a description",
            },
            "picture": {
                "alt": "A picture used to identify this workspace",
                "no-picture": "No picture uploaded.",
                "label": "Upload a picture",
                "remove-picture": "Remove picture",
            },
        },
        "workspace-users": {
            "title": "Workspace users",
            "search": {
                label: "Search workspace users",
                placeholder: "Enter a query to search for workspace users",
            },
            "no-job-title": "No job title",
            "no-workspace-users-found":
                "No workspace users found for this search query. Please try another search.",
            "role": "Role",
            "workspace-user-details": "Workspace user details",
            "invite-new-workspace-users": "Invite new workspace users",
            "actions": {
                action: "Action",
                remove: "Remove",
            },
        },
        "billing": {
            "title": "Billing",
            "active": {
                "status": {
                    title: "Current subscription status",
                    explanation: "Your subscription is currently active",
                },
                "monthly-total": {
                    title: "Monthly total ({pricePerSeat, number, ::currency/USD} per seat/month):",
                    status: "{total, number, ::currency/USD}",
                },
                "seats": {
                    title: "Number of seats:",
                    status: "{seats} seats in total, {seatsRemaining} {seatsRemaining, plural, one {seat} other {seats}} remaining",
                },
                "edit-billing-details": "Edit billing details",
            },
            "unpaid": {
                status: {
                    title: "Trial mode",
                    explanation:
                        "You are currently using this workspace in trial mode. To create a subscription and use all available features for this workspace, please continue using the checkout below. Alternatively, you can enter a coupon code further below.",
                },
                checkout: {
                    title: "Checkout",
                    seats: {
                        explanation:
                            "Select the amount of workspace seats. For each workspace user that is invited or added, a seat is used up.",
                        placeholder: "Number of workspace seats",
                        label: "Workspace seats",
                    },
                    action: "Go to checkout",
                },
                coupon: {
                    "title": "Use a coupon code",
                    "description":
                        "If someone has given you a coupon code, you can use it here to upgrade your workspace. Please refer to the details given to you for more information on what features will be unlocked for your workspace. If you have any questions, please ask the person who gave you the coupon code or contact us.",
                    "code": {
                        placeholder: "Enter coupon code",
                        label: "Coupon code",
                    },
                    "unknown-error": "An unknown error has occured",
                    "action": "Redeem coupon code",
                },
            },
            "custom": {
                status: {
                    title: "Custom subscription active",
                    explanation:
                        "You have activated a custom subscription for this workspace using a coupon code. If you have any questions about your subscription or if you would like to make changes, please contact us.",
                },
            },
            "contact-us":
                "Contact us if you have any questions regarding billing.",
            "billing-contact": "hello@projectifyapp.com",
        },
    },
    "index": {
        hero: {
            header: "Manage projects the right way.",
            text: "Warp drive your way to success with software that helps you to collaborate on and manage projects efficiently, with speed.",
            button: "Start a free trial",
            alt: "An illustration showing the look and feel of tasks in Projectify's user interface",
        },
        trust: {
            header: 'Everything you need to <span class="text-primary">stay organized</span> and <span class="text-primary">deliver faster</span>',
            text: "The go-to project management tool for developers.",
        },
        features: {
            "feature-1": {
                header: "Task cards that are accessible and keyboard friendly",
                text: "No more drag and drop disasters! Create and move tasks around the board with ease and speed. Organize and prioritize your workload with peace of mind.",
                alt: "A screenshot from the Projectify dashboard showing how the interface can be used without drag and drop",
            },
            "feature-2": {
                header: "Transform mammoth tasks into smaller, feasible ones",
                text: "Sub tasks break up the workload to allow for large tasks and progress to become more realistic and achievable. Add, reorder, edit and delete limitless sub tasks.",
                alt: "A screenshot from a task in the Projectify UI showing how sub tasks can be assigned to tasks",
            },
            "feature-3": {
                header: "Full control of your workspaces",
                text: "List and column views allow you to organize workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, workspace users, or keywords to focus on specific tasks.",
                alt: "An illustration showing how tasks can be filtered by workspace users or labels",
            },
            "feature-4": {
                header: "Keep an eye on important updates",
                text: "Whether it's a question about a task, a change of assignee, or simply a task moving to the next stage of development, notifications immediately let you know when there's an update.",
                alt: "An illustration showing notifications in the Projectify UI informing the user of recent updates to their tasks",
            },
            "feature-5": {
                header: "Responsive for on-the-go",
                text: "Need to access your projects while away from the office? No app. No problem. A fully responsive experience to stay connected and keep projects on track.",
                alt: "An illustration of a smartphone showing the Projectify UI in a landscape orientation.",
            },
            "feature-6": {
                header: "We never sell your data. Ever.",
                text: "Our platform fully complies with GDPR regulations, amongst others, so you can be rest assured that your private information stays private.",
                alt: "An illustration showing our mascot Poly safekeeping your data",
            },
            "feature-7": {
                header: "Projectify is 100% Free Software",
                text: "We respect your freedom and privacy and provide you the source code under a Free Software license. The Projectify application is licensed under the GNU Affero General Public License (AGPL) version 3.0 or later.",
                link: "Learn more here",
                alt: "Birds freed from their gilded cage",
            },
        },
        solutions: {
            header: {
                title: "Meeting diverse needs with practical solutions.",
                text: "From companies big and small to individuals working alone, Projectify can be used to manage all kinds of tasks.",
            },
            list: {
                "development-teams": {
                    text: "Development teams",
                    alt: "An illustration showing our mascot Poly working at a computer",
                },
                "research": {
                    text: "Research",
                    alt: "An illustration showing our mascot researching in a laboratory",
                },
                "project-management": {
                    text: "Project management",
                    alt: "An illustration showing our mascot overseeing our factory",
                },
            },
            more: "See more use cases",
        },
    },
    "pricing": {
        "header": {
            title: "Pricing",
            subtitle: "One plan. One price. All features.",
        },
        "plan": {
            title: "Universal Plan",
            price: "{price, number, ::currency/USD} / seat per month",
            cta: "Start a free trial",
        },
        "features": {
            title: "What's included?",
            list: [
                "Unlimited tasks",
                "Unlimited workspace boards",
                "Collaborate with workspace users",
                "Add multiple labels",
                "Role permissions",
                // "Set due dates",
                "Customize your workspace",
                "Archive completed workspace boards",
                // "Real-time notifications",
                // "File storage of 3 GB",
                "Filter by label or assignee",
                "Accessible interface",
            ],
        },
        "trial-mode": {
            title: "Trial mode available",
            explanation:
                "You can use a Projectify workspace in trial mode free of charge. The trial allows you to evaluate whether the Projectify project management software suits your needs. While your workspace is in trial mode, the following limitations will apply.",
            limitations: {
                title: "Trial mode limitations",
                list: [
                    // TODO mention chat messages when available -
                    "A workspace can have up to <strong>2</strong> workspace users",
                    "A workspace can hold up to <strong>10</strong> workspace boards",
                    "You can create up to <strong>100</strong> workspace board sections",
                    "You can create up to <strong>1000</strong> tasks",
                    "You can create up to <strong>1000</strong> sub tasks",
                    "You can create up to <strong>10</strong> labels",
                ],
            },
        },
    },
    "solutions": {
        "index": {
            hero: {
                title: "Solutions for every type of user",
                text: "Explore the different ways users are using Projectify to meet due dates, reach targets and be productive.",
                illustration: {
                    alt: "An illustration showing users of different backgrounds",
                },
            },
            solutions: {
                "development": {
                    title: "Development teams",
                    description:
                        "Monitor team progress throughout the whole software lifecyle.",
                    illustration: {
                        alt: "Our mascot Poly sitting in front of a computer, developing software and looking content",
                    },
                },
                "research": {
                    title: "Research",
                    description:
                        "Keep track of testing processes and results with incredible detail.",
                    illustration: {
                        alt: "Two content looking Polys (our mascot) researching in a laboratory and taking down notes on a chalkboard",
                    },
                },
                "project-management": {
                    title: "Project management",
                    description:
                        "Faciliate rapid delivery across multiple projects for any industry.",
                    illustration: {
                        alt: "Two Polys in a factory pointing at machines symbolized by huge gears. The mascot on the left holds a wrench.",
                    },
                },
                "academic": {
                    title: "Academic endeavours",
                    description:
                        "Structure a thesis, organise a project or keep track of assignments.",
                    illustration: {
                        alt: "Our mascot Poly celebrating their graduation from an educiational institution, wearing an academic dress, throwing a square academic cap into the air",
                    },
                },
                "remote-work": {
                    title: "Remote work",
                    description:
                        "Asynchronous communication whether you're at home or away.",
                    illustration: {
                        alt: "Our mascot Poly working at the beach looking happy",
                    },
                },
                "personal-use": {
                    title: "Personal use",
                    description:
                        "Log an exercise routine, create a new diet or plan an adventure. The possibilities are endless.",
                    illustration: {
                        alt: "Our mascot Poly thinking about all the things they want to do, among them being running, taking pictures and eating something tasty, each thing symbolized by a thought bubble",
                    },
                },
            },
            more: "Learn more",
        },
        "development": {
            hero: {
                title: "Development solutions",
                text: "How development teams can use Projectify to create tasks, monitor pulls requests and deploy faster.",
            },
            features: {
                "feature-1": {
                    title: "Organise with labels and task numbers",
                    text: "Use labels with terms like bug, enhancement or backend to categorize tasks. Filter with labels or search by task number to quickly locate what you're looking for.",
                    illustration: {
                        alt: "A illustration showing the label context menu used in Projectify",
                    },
                },
                "feature-2": {
                    title: "Live notifications",
                    text: "Notifications provide you with all the information you need whilst also giving you conveniant 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
                    illustration: {
                        alt: "An illustration showing the live notifications a user can receive in Projectify",
                    },
                },
                "feature-3": {
                    title: "Plan and execute",
                    text: "Set up and monitor pull requests, merges, bug fixes and more for multiple workspace users of your team.",
                    illustration: {
                        alt: "An illlustration showing tasks in a section called 'In Progress'",
                    },
                },
            },
        },
        "research": {
            hero: {
                title: "Research solutions",
                text: "How researchers teams can use Projectify to collaborate on data with colleagues and meticulously catalogue findings.",
            },
            features: {
                "feature-1": {
                    title: "Categorize data with labels and numbers",
                    text: "Labels simplify the process of categorizing tasks. Automatically assigned task numbers take organisation one step further",
                    illustration: {
                        alt: "An illustration showing tasks in a section called 'In Progress'",
                    },
                },
                "feature-2": {
                    title: "Provide and request updates on any task",
                    text: "The updates sections allows you and your colleagues to share new details about how a test, experiment or study has gone.",
                    illustration: {
                        alt: "An illustration showing updates posted in a task by various users discussing organizing a meeting",
                    },
                },
                "feature-3": {
                    title: "Create and monitor multiple projects",
                    text: "With unlimited project boards and tasks per workspace, you're free to perform as much research and testing as you require.",
                    illustration: {
                        alt: "An illustration suggesting the different ways labels can be assigned to different team members depending on their role, such as design or marketing",
                    },
                },
            },
        },
        "project-management": {
            hero: {
                title: "Project management solutions",
                text: "How project managers can use Projectify to efficiently manage tasks, projects and workspace users of their team.",
            },
            features: {
                "feature-1": {
                    title: "An ethical approach to management",
                    text: "View how many tasks a workspace user has assigned to them, so the workload can be divided equally. Filter by workspace user to see what individual colleagues are working on.",
                    illustration: {
                        alt: "An illustration showing how Projectify displays each workspace users assigned task count",
                    },
                },
                "feature-2": {
                    title: "Live notifications",
                    text: "Notifications provide you with all the information you need whilst also giving you convenient 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
                    illustration: {
                        alt: "An illustration showing notifications arriving about tasks being updated",
                    },
                },
                "feature-3": {
                    title: "Full control of your workspaces",
                    text: "List and column views allow you to organise workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, users or keyboards to focus on specific tasks.",
                    illustration: {
                        alt: "An illustration showing a collapsed dashboard side bar and various workspace users and labels",
                    },
                },
                "feature-4": {
                    title: "Permissions to control access",
                    text: "Make sure nothing important gets deleted. With permission roles - Owner, Maintainer, Member and Observer, you can be safe in knowing there won't be any accidentally data loss.",
                    illustration: {
                        alt: "An illustration of a settings screen showing workspace users belonging to a workspace user and their role within the workspace. The illustration also shows a button allowing filtering by role and another button letting a user invite new workspace users",
                    },
                },
            },
        },
        "academic": {
            hero: {
                title: "Academic solutions",
                text: "How students can use Projectify to plan a thesis, collaborate, or keep track of assignments.",
            },
            features: {
                "feature-1": {
                    title: "Deadlines become a lifeline",
                    text: "Projectify notifies you of upcoming due dates for assignments, so you'll never miss a paper's due date.",
                    illustration: {
                        alt: "An illustration showing how Projectify will inform a user of different task due dates and other important updates",
                    },
                },
                "feature-2": {
                    title: "Checklists that aid your progress",
                    text: "We know that projects and dissertations can be daunting, but we're here to help. Breaking tasks into smaller sub tasks allow you to micro-achieve your way to completion.",
                    illustration: {
                        alt: "An illustration showing how users can track subtask progress for each task",
                    },
                },
                "feature-3": {
                    title: "Create notes on each task and coordinate with friends",
                    text: "Invite friends and classmates into your workspace to collaborate, share ideas and more.",
                    illustration: {
                        alt: "An illustration showing the various features the task view has to offer, such as description, sub tasks, tracking task updates, and more",
                    },
                },
            },
        },
        "remote-work": {
            hero: {
                title: "Remote solutions",
                text: "How remote workers can use Projectify to keep in tune with projects and stay connected.",
            },
            features: {
                "feature-1": {
                    title: "Work together across timezones",
                    text: "Asynchronous communication is vital for all teams be they remote or in the office. Assign tasks, create new projects and provide updates, anywhere, anytime.",
                    illustration: {
                        alt: "An illustration showing the updates screen of a task where two workspace users decide on when to organize a remote meeting",
                    },
                },
                "feature-2": {
                    title: "Notifications and updates on any task",
                    text: "Notifications allow for important information to be delivered, even if you're not around. When you're away from your computer, updates to task will stay unread in the notification center until you get back.",
                    illustration: {
                        alt: "An illustration showing a notification popup telling the user about recent updates to the tasks in their workspace",
                    },
                },
                "feature-3": {
                    title: "Assign tasks to users all over the world",
                    text: "Whether it's Leo in the Phillipines or Valerie in Brazil, once you assign a task to someone they will be notified immediately with a pop-up.",
                    illustration: {
                        alt: "An illustration showing the 'In Progress' section of a workspace board with tasks being assigned to different users",
                    },
                },
            },
        },
        "personal-use": {
            hero: {
                title: "Personal solutions",
                text: "How people can use Projectify for everyday life, whether it be keeping track fo your health or creating an itinerary for a trip.",
            },
            features: {
                "feature-1": {
                    title: "Create tasks with ease",
                    text: "Organise your tasks into individual projects with sections such as 'To do', 'In progress' and 'Done'. Provide descriptions for each task and set due dates. Labels simplify the process of catergorizing tasks.",
                    illustration: {
                        alt: "An illustration showing a 'To do' and 'Done' section, showing personal tasks that a user assigned to themselves, such as 'Book a ticket to Paris' or 'Learn French for beginners'",
                    },
                },
                "feature-2": {
                    title: "Check off sub tasks as you go",
                    text: "Need to plan an event? Want to create a list of achievements? Sub tasks help you to check off small tasks bit by bite.",
                    illustration: {
                        alt: "An illustration showing various sub tasks that a user has created within a task, such as 'Swim freestyle for 10 lengths'",
                    },
                },
                "feature-3": {
                    title: "Add friends and family to your space",
                    text: "Get everyone on the same page by assigning task to different workspace users.",
                    illustration: {
                        alt: "An illustration showing how different tasks in the 'In progress' section of a workspace board have been assigned to friends and family. The tasks are 'Trim back overgrown hedges', 'Polish wooden furnishings', and 'Replace extractor fan grating'",
                    },
                },
            },
        },
    },
    "terms-of-service": {
        nav: {
            "title": "Terms of service",
            "japanese": "Japanese (original)",
            "english": "English (translation)",
            "go-back": "Jump back to top",
        },
    },
    "privacy-policy": {
        nav: {
            "title": "Privacy Policy",
            "japanese": "Japanese Privacy Policy (original)",
            "english": "English Privacy Policy (translation)",
            "japanese-gdpr": "Japanese GDPR Privacy Policy (original)",
            "english-gdpr": "English GDPR Privacy Policy (translation)",
            "go-back": "Jump back to top",
        },
    },
    "free-software": {
        "hero": "Free Software and License Information",
        "header": "Projectify project management software is created by:",
        "license":
            "This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
        "warranty":
            "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.",
        "find-copy":
            "You can retrieve a copy of the source code and the LICENSE here:",
        "source": {
            frontend: "Projectify Frontend",
            backend: "Projectify Backend",
        },
        "trademark": "<strong>Projectify</strong> is a registered trademark.",
    },
    "contact-us": {
        title: "Contact",
        body: {
            title: "Contact information",
            text: "Should you have any questions, suggestions, or other inquiries regarding Projectify, please contact us using the following email address written below. We try to answer all inquiries within two working days. Please be patient if it takes longer.",
        },
        email: {
            href: "mailto:hello@projectifyapp.com?subject=Projectify contact",
            label: "hello@projectifyapp.com",
        },
        illustration: {
            alt: "An illustration of a phone booth",
        },
    },
    "accessibility": {
        hero: {
            title: "Accessibility statement",
            illustration: {
                alt: "Accessibility logo",
            },
        },
        goals: {
            title: "Accessibility goals",
            text: "Projectify is committed to ensuring digital inclusivity and accessibility for people with diverse disabilities. We are continually improving the user experience for everyone, and applying the relevant accessibility standards. We are also aiming to improve the use of both our website and platform for users who employ assistive technologies.",
        },
        measures: {
            title: "Measures we take to support accessiblity",
            list: [
                "Include accessibility as part of our mission statement",
                "Ensure designs meet a minimum accessibilty level (WCAG 2.1 level AA)",
                "Compatibility with different web browsers and assistive technology",
                "Include people with disabilities in our user personas",
                "Conduct usability tests with people who have disabilities",
            ],
        },
        conformance: {
            title: "Conformance status",
            text: "The Web Content Accessibility Guidelines (WCAG) standard defines requirements to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA. 'Fully conforms' means that the content meets all of the WCAG requirements at the specified Level without exceptions. Although our goal is WCAG 2.1 Level AA conformance, we have also applied some Level AAA Success Criteria: Images of text are only used for decorative purposes. Content posted since May 2022 fully conforms to WCAG 2.1 Level AA. It partially conforms to Level AAA.Older content conforms to earlier versions of WCAG, for example, WCAG 2.0.",
        },
        compatibility: {
            title: "Compatibility with browsers and assistive technologies",
            text: "The Projectify website and platform is designed to be compatible with assistive technologies and the last two versions of major browsers. The website and platform are not designed for Internet Explorer 11 and earlier versions.",
        },
        platform: {
            title: "Platform",
            text: "We are currently in the process of making our platform conform to accessiblity standards. Our main focus is to improve color contrast in both the light and dark modes of our platform, increase discoverability of features for users with vision impairments and enhance the usability of our main components.",
        },
        website: {
            title: "Website",
            list: [
                "Keyboard navigation: All menus, buttons , inputs and actions are accessible from a keyboard",
                "Screen reader compatibility: Our code supports the use of screen readers for users who digest information through audio means",
                "Images: All images are supported with descriptive and accurate alternative text which can be read by screen readers",
                "Text: Our text size, weight and font style have been carefully chosen to be accessible to users with dyslexia and/or visual impairment. WCAG 2.0 level AA requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text.",
                "Color: WCAG 2.1 requires a contrast ratio of at least 3:1 for graphics and user interface components, which we meet",
                "Magnification: For sight impaired users, all pages and content can be magnified using standard browser controls or magnification software",
            ],
        },
        limitations: {
            title: "Limitations",
            text: "We are aware that, despite our best efforts, there may be limitations to the accessibilty of both the platform and website. Below is a description of known limitations. Please contact us if you discover an issue not listed below. Known limitations of the platform:",
            list: [
                "Tab selection not working on the calendar menu",
                "Not all screen readers can read placeholder text",
            ],
        },
        evaluation: {
            title: "Evaluation report",
            text: "An evaluation report can be found here link. Assessment of both the platform and website was carried out by self-evaluation.",
        },
        contact: {
            title: "Contact us",
            text: "We welcome feedback on the accessibility of Projectify. If you encounter any acccessibility barriers whilst using the platform or website, please email hello@projectify.com. ",
        },
    },
    "help": {
        "hero": {
            image: {
                alt: "Our mascot poly flying into the air using a jetpack",
            },
            header: {
                text: "Help and tips",
                subtext:
                    "Learn to fly through projects with speed and agility",
            },
        },
        "overview": "Overview",
        "help-sections": "Help sections",
        "go-to-section": "View this section",
        "basics": {
            title: "Basics",
            description: "Your first steps towards productivity",
            sections: [
                {
                    id: "workspace",
                    title: "What is a workspace?",
                    content:
                        "A workspace is an area where you can create projects, tasks, labels and invite various members of your organisation as workspace users. In a workspace you can set permissions and customise the overall look and feel of your productivity center. For more information on workspaces please see Workspaces.",
                },
                {
                    id: "workspace-board",
                    title: "What is a board?",
                    content:
                        "A board is a specific project in your workspace that you would like to work on.You can create unlimited boards per workspace and have the freedom to rename and organise them.Completed boards can be archived to remove clutter from your workspace. For more information on boards please see Boards.",
                },
                {
                    id: "workspace-board-section",
                    title: "What is a section?",
                    content:
                        "A section is a category that you can divide tasks into. Popular categories include ‘To do’ ‘In progress’ and ‘Done’. Sections can be moved and edited freely. For more information on sections please see Sections.",
                },
                {
                    id: "task",
                    title: "What is a task?",
                    content:
                        "A task is a step in your project that needs to be completed. Tasks can be assigned to any workspace user in your workspace. Labels and detailed information can be applied to tasks. For every task that is created, a unique task number is assigned to it for ease of reference and searching. Tasks can be further divided into sub tasks - sub tasks are great for keeping track of micro achievements per task. Due dates can also be set for tasks that need to be completed on a due date. For more information on tasks please see Tasks.",
                },
                {
                    id: "side-menu",
                    title: "How to use the side menu",
                    content:
                        "The side menu allows for full control of your workspace and projects.You are able to switch between workspaces or boards through this menu. Filtering between workspace users and labels can also be performed here.Workspace settings such as permissions and billing can be accessed from this menu.The menu can be viewed in full expanded mode or in collapsed mode.",
                },
            ],
        },
        "workspaces": {
            title: "Workspaces",
            description: "Independent spaces at your fingertips",
            sections: [
                {
                    id: "create-workspace",
                    title: "Create a workspace",
                    content:
                        "When you make an account with Projectify you will automatically have one workspace created for you. To create more workspaces, click the workspace dropdown in the side menu. This will open up a sub menu where you can click the Add new workspace button.",
                },
                {
                    id: "switch-workspaces",
                    title: "Switch workspaces",
                    content:
                        "To switch between workspaces, click the workspace dropdown in the side menu. This will open up a sub menu where you can switch between different workspaces associated with your account.",
                },
                {
                    id: "workspace-settings",
                    title: "Workspace settings",
                    content:
                        "To go to workspace settings, click the ellipsis next to the workspace button in the side menu. This will open up a sub menu where you can access the current workspaces settings page.Workspace settings consists of three tabs. General, workspace users and billing. General provides information on your current workspace such as the name of the workspace. Workspace users allows you to add, edit permissions and delete workspace users. Billing provides a way for you to amend your account billing details.",
                },
                {
                    id: "delete-workspace",
                    title: "Delete a workspace",
                    content:
                        "To delete a workspace, first click the workspace dropdown button to select the correct workspace. Then, click the ellipsis next to the workspace button in the side menu. This will open up a sub menu where you can access the current workspaces settings page.In the General tab you will find a button at the bottom of the page that gives you the option to delete this workspace.Be aware that if you only have one workspace, deleting your workspace will also delete your account.",
                },
            ],
        },
        "workspace-boards": {
            title: "Workspace boards",
            description: "Separate projects from each other",
            sections: [
                {
                    id: "create-workspace-board",
                    title: "Create a workspace board",
                    content:
                        "To create a board, click the Add New Board button in the side menu. You can cycle through the different boards in your workspace easily by clicking each board button.",
                },
                {
                    id: "edit-workspace-board",
                    title: "Edit a workspace board",
                    content:
                        "To edit a workspace board, hover over the workspace board and click the ellipsis button that appears. This will bring up a sub menu with an option to edit the board. Click Edit board to bring up an overlay that allows you to edit the board name.",
                },
                {
                    id: "archive-workspace-board",
                    title: "Archive a workspace board",
                    content:
                        "To archive a workspace board, hover over the workspace board and click the ellipsis button that appears. This will bring up a sub menu with an option to archive the workspace board. Click Archive workspace board to bring up an overlay that allows you to archive the board.",
                },
                {
                    id: "delete-workspace-board",
                    title: "Delete a workspace board",
                    content:
                        "To delete a workspace board, first navigate to the workspace board archive. You can reach the workspace board archive by clikcing on the ellipsis menu button next to the workspace selector. It appears as three blue dots inside a blue circle. From there a context menu opens, where you can click on ''Go to archive'' to go to the workspace board archive. Once you reach the workspace board archive from there, you can either recover a workspace board or permanently delete it. When you recover a workspace board, it will be put back next to the other workspace boards in your side navigation. When you delete a workspace board, all the workspace boards sections and tasks contained within will be deleted as well.",
                },
            ],
        },
        "workspace-board-sections": {
            title: "Workspace board sections",
            description: "Maximize the efficiency of your tasks",
            sections: [
                {
                    id: "create-workspace-board-section",
                    title: "Create a workspace board section",
                    content:
                        "To create a workspace board section click the + icon in the top right corner. This will bring up an overlay for you to give the workspace board section a name.",
                },
                {
                    id: "workspace-board-section-navigation",
                    title: "Workspace board section navigation",
                    content:
                        "On the right side of the dashboard you will find a number of dots that indicate how many workspace board sections you have created on this workspace board. The current workspace board section you are focused on with have its dot extended. Click the dots to quickly navigate through to another workspace board section. This is particularly useful when you have a lot of tasks in each workspace board section.",
                },
                {
                    id: "workspace-board-section-context-menu",
                    title: "Workspace board section context menu",
                    content:
                        "The workspace board section context menu gives you the option to: Expandind or collapsing the workspace board section, swapping positions with the previous or next workspace board section, creating a new task within that workspace board section, edit the workspace board section, and deleting the workspace board section",
                },
                {
                    id: "move-workspace-board-section",
                    title: "Move a workspace board sections",
                    content:
                        "To move a workspace board section, click the ellipsis in the right corner of the workspace board section. This will bring up a sub menu with the options mentioned above in 'workspace board section context menu'. You can either switch the workspace board section with the previous or the next workspace board section.",
                },
                {
                    id: "edit-workspace-board-section",
                    title: "Edit a workspace board section",
                    content:
                        "To edit a workspace board section, click the ellipsis in the right corner of the section. This will bring up a context menu with the options mentioned in 'Workspace board section context menu'. Click 'Edit workspace board section' to edit the name of the workspace board section.",
                },
                {
                    id: "delete-workspace-board-section",
                    title: "Delete a workspace board section",
                    content:
                        "To delete a workspace board section, click the ellipsis in the right corner of the workspace board section. This will bring up a context menu with the options mentioned in 'Workspace board section context menu'. Click 'Delete workspace board section' to bring up an overlay where you can confirm your decision to delete the workspace board section.",
                },
            ],
        },
        "tasks": {
            title: "Tasks",
            description: "All the ins and outs of task creation",
            sections: [
                {
                    id: "create-task",
                    title: "Create a task",
                    content:
                        "Tasks are the backbone of Projectify. In order to create a task simply click the + (plus) icon in a workspace board section panel. If you do not know how to create a workspace board section, please see the help page on workspace board sections. Another way of creating a task is to click the ellipsis button in the workspace board section panel, then click on 'Add a new task'",
                },
                {
                    id: "add-context-to-task",
                    title: "Add context to a task",
                    content:
                        "Context could be in the form of a title, description, label, assignee or due date. You have the freedom to add as little or as much context as you want, however we require having a title at the very least. When you create a task, an input form allows you to input information about the task.",
                },
                {
                    id: "edit-task",
                    title: "Edit a task",
                    content:
                        "Once a task has been saved, you can go back in and edit the task by click the task. This will open up the same menu mentioned in the previous section above. You can also open this page with the task ellipsis button on the far right. Click in each field to edit the content you previously entered and once youre done, dont forget to save your work!",
                },
                {
                    id: "move-task",
                    title: "Move a task",
                    content:
                        "There are a few ways you can move a task as well as a few places. You can move your tasks around inside the workspace board section they are housed in as well as move them to other workspace board sections in your workspace board. For example, if you have a workspace board section called 'To Do' and another workspace board section called 'In Progress', you can move tasks between these workspace board sections. Moving tasks is simple. On the right of a task are three buttons. An up button, a down button and an ellipsis (three dots) button. The up and down buttons move the task inside the workpace board section. The ellipsis button allows you to select a workspace board section to move the task to, as well as more actions inside the current workspace board section such as 'Move to top' and 'Move to bottom'.",
                },
                {
                    id: "delete-task",
                    title: "Delete a task",
                    content:
                        "In order to delete a task, click the ellipsis button in the task card and select 'Delete task' from the dropdown. This will open an overlay for you to confirm your choice to delete this task.",
                },
                // TODO mention bulk delete in delete-task
            ],
        },
        "labels": {
            title: "Labels",
            description: "Create categories for your tasks",
            sections: [
                {
                    id: "create-label",
                    title: "Create a label",
                    content:
                        "Labels allow you to bring some organisation to your tasks. To create a label, click the label button in the side menu and then click the 'Create new label' button. This will open up a new menu where you can write the name of your new label as well as choose a color for it. Click the 'Save label' button to create your new label. Another way to create a label is when you are creating a new task.",
                },
                {
                    id: "apply-label-to-task",
                    title: "Apply a label to a task",
                    content:
                        "There are two ways to apply a label to a task. If you are creating a task for the first time, you have the option to apply a label to the task in the context menu. You will find this button in the top right corner next to the title.If you have created a task but haven't applied a label to it yet. Click the apply label button on the task card. This will open up a menu with your labels so that you can select the appropriate one for your task.",
                },
                {
                    id: "edit-label",
                    title: "Edit a label",
                    content:
                        "Open the side menu and click the label button. Hover over any label and click the edit button that appears. This will open the same menu as creating a label, but this time the name and color will be filled in. From here you can edit the name of the label as well as change the color of the label. Click the save label button to keep your changes.",
                },
                {
                    id: "filter-by-labels",
                    title: "Filter by labels",
                    content:
                        "You can filter and search labels that you have created by using the side menu. Searching for labels helps you to find a label quickly and filtering by label allows you to see similar tasks at the same time. You can apply more than one filter at a time. Click the label button in the side menu and from there you can either search for a label or filter labels.",
                },
                {
                    id: "delete-label",
                    title: "Delete a label",
                    content:
                        "In order to delete a task, click the label section in the side menu and hover over any label. Click the delete icon that appears and confirm your choice to delete this label.",
                },
                // TODO "Ways to use labels"
            ],
        },
        "workspace-users": {
            title: "Workspace users",
            description: "Collaboration starts with an invite",
            sections: [
                {
                    id: "invite-a-workspace-user",
                    title: "Invite a workspace user",
                    content:
                        "To invite a workspace user to your workspace click the workspace users button in the side menu. Then click the 'Add new workspace user' button. This will take you to a new page away from the dashboard called Workspace settings. This page can be found in the ellipsis next to the workspace dropdown in the side menu. From this page, you can send invites for workspace users to access your workspace by entering their email addresses. We'll take care of the rest. Be aware that you will not be able to invite workspace users if you do not have enough seats available in your workspace.",
                },
                {
                    id: "assign-task-to-workspace-user",
                    title: "Assign a task to a workspace user",
                    content:
                        "There are two ways to apply a label to a task. If you are creating a task for the first time, you have the option to assign it to a workspace user in the context menu. You will find this assign workspace user button in the top left corner next to the title. If you have created a task but haven't assigned it to a workspace user yet. Click the assign workspace user button on the task card. This will open up a menu with a list of your workspace users so that you can select the appropriate one for the task.",
                },
                {
                    id: "filter-workspace-user",
                    title: "Filter by workspace user",
                    content:
                        "You can filter and search workspace users that are part of your workspace by using the side menu. Searching for workspace users helps you to find a workspace user quickly and filtering by workspace users allows you to see tasks a certain workspace user is working on. You can apply more than one filter at a time. Click the workspace user button in the side menu and from there you can either search for a workspace user or filter workspace users. Filtering a workspace user also allows you to see how many tasks that workspace user has assigned to them. This feature is great in determing which team workspace users are available for new tasks to be assigned to them.",
                },
                {
                    id: "edit-workspace-user-permissions",
                    title: "Edit a workspace user's permissions",
                    content:
                        "To edit workspace user permissions, click the ellipsis button in the side menu.This will open up the workspace settings page. Click workspace users and from here you can search",
                },
                {
                    id: "delete-workspace-user",
                    title: "Delete a workspace user",
                    content:
                        "To delete a workspace user, click the ellipsis button in the side menu. This will open up the workspace settings page. Click the workspace user tab and from here you can search for workspace users and edit their permissions. For more on permissions, please see our guide on workspace user roles and permissions.",
                },
            ],
        },
        // TODO Bulk select
        "filters": {
            title: "Filters",
            description: "Streamline your workflow with filters",
            sections: [
                {
                    id: "filter-and-search-by-workspace-user",
                    title: "Filter and search by workspace user",
                    content:
                        "You can filter and search workspace users that are part of your workspace by using the side menu. Searching for workspace users helps you to find a workspace user quickly and filtering by workspace user allows you to see tasks a certain workspace user is working on. You can apply more than one filter at a time. Click the workspace user button in the side menu and from there you can either search for a workspaceu or filter workspace users. Filtering a workspace user also allows you to see how many tasks that workspace user has assigned to them. This feature is great in determing which team workspace users are available for new tasks to be assigned to them.",
                },
                {
                    id: "filter-and-search-by-label",
                    title: "Filter and search by label",
                    content:
                        "You can filter and search labels that you have created by using the side menu. Searching for labels helps you to find a label quickly and filtering by label allows you to see similar tasks at the same time. You can apply more than one filter at a time. Click the label button in the side menu and from there you can either search for a label or filter labels.",
                },
                {
                    id: "search-by-keyword",
                    title: "Search by keyword",
                    content:
                        "The search bar located in the header gives you the ability to further narrow down tasks by their title. Start typing any text and matching results will be automatically displayed below as you type. Clear your search by pressing the 'X' button to the right of the search input.",
                },
            ],
        },
        "billing": {
            title: "Billing and accounts",
            description: "Payment and account information",
            sections: [
                {
                    id: "billing-settings",
                    title: "Billing settings",
                    content:
                        "To go to workspace settings, click the ellipsis next to the workspace button in the side menu. This will open up a sub menu where you can access the current workspace’s settings page. From this page, you can access the billing settings of your account.",
                },
                {
                    id: "removing-adding-workspaces",
                    title: "Removing/adding workspaces",
                    content:
                        "Only users with the permission role of Owner can create and delete workspaces. You will need to provide your banking details for each workspace you create.",
                },
                {
                    id: "removing-adding-workspace-users",
                    title: "Removing/adding workspace users",
                    content:
                        "Only users with the permission role of Owner can invite or remove users. Be aware that you will not be able to invite workspace users if you do not have enough seats available in your workspace. In order to add more seats, please amend the seat numbers in your account.",
                },
                {
                    id: "",
                    title: "Delete your account",
                    content:
                        "To delete your account visit the billing page in workspace settings and cancel your subscription. Deleting your account will also remove workspace users from any workspaces that you own. You can transfer ownership of the account to a different workspace user before deletion to ensure that content and workspace users can continue to use the workspace. Deleting your account without transferring ownership will delete all data including personal information and all content created on the platform will cease to exist.",
                },
            ],
        },
        "skip": "Skip ahead to",
    },
    "navigation": {
        header: {
            "development-preview": "Development preview",
            "logo": {
                alt: "Projectify",
            },
            "solutions": "Solutions",
            "help": "Help",
            "pricing": "Pricing",
            "log-in": "Log in",
            "start-a-free-trial": "Start a free trial",
            "continue-to-dashboard": "Continue to dashboard",
        },
        footer: {
            logo: {
                alt: "Projectify",
                heading: "Project management at pace.",
            },
            cta: "Start a free trial",
            nav: {
                product: {
                    title: "Product",
                    pricing: "Pricing",
                },
                resources: {
                    "title": "Resources",
                    "help-and-tips": "Help and tips",
                },
                company: {
                    "title": "Company",
                    "accessibility-statement": "Accessibility statement",
                    "contact-us": "Contact us",
                    "corporate-info": "Corporate information",
                },
                legal: {
                    "title": "Legal",
                    "privacy": "Privacy Policy",
                    "tos": "Terms of Service",
                    "free-software": "Free Software",
                },
            },
            epilogue: {
                "copyright": "Copyright 2021-2024 JWP Consulting GK",
                "free-software":
                    "The Projectify application is free software, and you are welcome to redistribute it under certain conditions;",
                "details": "see here for details",
                "build":
                    "This version was built on {buildDate} from commit {commitHash} on branch {branchName} committed on {commitDate}.",
            },
        },
    },
    "roles": {
        observer: "Observer",
        member: "Member",
        maintainer: "Maintainer",
        owner: "Owner",
    },
    "typography": {
        anchor: {
            "new-tab": "(Opens in new tab)",
        },
    },
};
export default messages;
