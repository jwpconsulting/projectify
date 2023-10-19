// TODO create a tool to show which message strings are unused
type Message = string | string[] | { [property: string]: Message };

type MessageCollection = Record<string, Message>;
// TODO prohibit root level strings
// TODO type MessageDirectory = Record<string, MessageCollection>;
// TODO const messages: MessageDirectory = {
const messages: MessageCollection = {
    "overlay": {
        constructive: {
            "update-workspace-board": {
                title: "Edit workspace board",
                form: {
                    title: {
                        label: "workspace board name",
                        placeholder: "Enter a workspace board name",
                    },
                    deadline: {
                        label: "deadline",
                        placeholder: "Select date",
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
                    deadline: {
                        label: "Deadline",
                        placeholder: "Select date",
                    },
                },
                "cancel": "Cancel",
                "create-board": "Create board",
            },
            "invite-workspace-user": {
                title: "Invite workspace users",
                notice: "You have 3 seats left in your plan",
                form: {
                    email: {
                        label: "Enter email address separated by a comma",
                        placeholder: "workspace-user@mail.com",
                    },
                },
                cancel: "Cancel",
                invite: "Invite",
            },
            "invite-workspace-user-error": {
                "title": "Invite workspace users",
                "notice": "You have no more seats left in your plan",
                "cancel": "Cancel",
                "go-to-billing": "Go to billing",
            },
            "create-workspace-board-section": {
                "title": "Create new section",
                "form": {
                    title: {
                        label: "New section name",
                        placeholder: "New section name",
                    },
                },
                "cancel": "Cancel",
                "create-section": "Create section",
            },
            "create-workspace": {
                "title": "Create a new workspace",
                "notice": "Are you sure you want to create a new workspace?",
                "cancel": "Cancel",
                "create-workspace": "Create workspace",
            },
            "skip-onboarding": {
                "title": "Skip onboarding",
                "notice": "Any progress you've made so far will be lost",
                "cancel": "Cancel",
                "skip-onboarding": "Skip onboarding",
            },
            "recover-workspace-board": {
                "title": "Recover this board?",
                "notice": "Recovering this board returns it to the dashboard",
                "cancel": "Cancel",
                "recover-board": "Recover board",
            },
        },
        // TODO Put other destructive dialogs here
        destructive: {},
    },
    "label": {
        "apply-label": "apply label",
    },
    "dashboard": {
        "dashboard": "dashboard",
        "create-board": "create new board",
        "boards": "boards",
        "workspace-users": "workspace-users",
        "labels": "labels",
        "workspace-user-name": "Workspace user name",
        "filter-workspace-users": "Filter workspace users",
        "search-task": "Search Task",
        "assign-user": "Assign user",
        "no-sections": {
            message: "There are no sections in this workspace board.",
            prompt: "Add a section",
        },
        "section": {
            empty: {
                message: "No tasks in this section.",
                prompt: "Add a task here",
            },
        },
        "no-user-assigned": "No user assigned",
        "error": {
            "title": "Error:",
            "description":
                "We apologize for the error. There was an error loading your dashboard. The error details are as follows:",
            "what-to-do": {
                message:
                    "Unfortunately this means we are unable to load this page properly. To help resolve this:",
                options: [
                    "Visit our troubleshooting section](XXX) for common solutions.",
                    "Contact [our support here](XXX) for help.",
                ],
            },
        },
    },
    "page404": {
        title: "Lost your way?",
        body: "The page you're looking for doesn't exist.",
        home: "Take me home",
    },
    "filter-label-menu": {
        "filter-labels": "Filter labels",
        "create-new-label": "Create new label",
        "label-name": "Label name",
        "save": "Save",
        "cancel": "Cancel",
    },
    "filter-label": {
        all: "all",
        none: "none",
    },
    "filter-workspace-user": {
        "all-users": "all users",
        "assigned-nobody": "assigned to nobody",
    },
    "select-board": {
        "edit-board": "edit board",
        "archive-board": "archive board",
    },
    "destructive-overlay": {
        "delete-label": "Delete label",
        "delete-label-body-1": "Would you like to delete the '",
        "delete-label-body-2": "' label?",
        "delete-label-button": "Delete",
        "delete-label-body-warning": "This action cannot be undone.",
        "delete-workspace-user": "Remove workspace user",
        "delete-workspace-user-body-1": "Would you like to remove '",
        "delete-workspace-user-body-2": "' from this workspace?",
        "delete-workspace-user-body-warning": "This action cannot be undone.",
        "delete-workspace-user-button": "Remove",
        "delete-section": "Delete section",
        "delete-section-body-1": "Would you like to delete the '",
        "delete-section-body-2": "' section?",
        "delete-section-body-warning":
            "Deleting this section will also delete all tasks within it.",
        "delete-section-button": "Delete",
        "delete-task": "Delete task",
        "delete-task-body-1": "Would you like to delete the '",
        "delete-task-body-2": "' task?",
        "delete-task-body-warning": "This action cannot be undone.",
        "delete-task-button": "Delete",
        "delete-selected-tasks": "Delete selected tasks",
        "delete-selected-tasks-body-1": "Would you like to delete ",
        "delete-selected-tasks-body-2": " selected tasks?",
        "delete-selected-tasks-body-warning": "This action cannot be undone.",
        "delete-selected-tasks-button": "Delete",
        "archive-board": "Archive board",
        "archive-board-body-1": "Would you like to archive this '",
        "archive-board-body-2": "' board?",
        "archive-board-body-warning":
            "You can see archived boards in the archives section",
        "archive-board-button": "archive",
        "delete-board": "Delete board",
        "delete-board-body-1": "Would you like to delete this '",
        "delete-board-body-2": "' board?",
        "delete-board-body-warning": "This action cannot be undone",
        "delete-board-button": "Delete",
        "cancel": "Cancel",
    },
    "profile-overlay": {
        "my-profile": "my profile",
        "log-out": "log out",
    },
    "workspace-overlay": {
        "add-new-workspace": "add new workspace",
    },
    "side-nav-overlay": {
        "help-tips": "Help & tips",
        "minimise-sidebar": "minimise sidebar",
        "expand-sidebar": "expand sidebar",
        "go-to-archive": "go to archive",
        "workspace-settings": "workspace settings",
    },
    "workspace-board-overlay": {
        "edit-board": "edit board",
        "archive-board": "archive board",
    },
    "workspace-board-section-overlay": {
        "expand-section": "expand section",
        "collapse-section": "collapse section",
        "switch-previous": "switch with previous section",
        "switch-next": "switch with next section",
        "edit-title": "edit section title",
        "add-task": "add task",
        "delete-section": "delete section",
    },
    "task-overlay": {
        "open-task": "open task",
        "move-to-section": "move to section",
        "move-to-top": "move to top",
        "move-to-bottom": "move to bottom",
        "copy-link": "copy link",
        "go-to-updates": "go to updates",
        "delete-task": "delete task",
    },
    "help-overlay": {
        "help-and-tips": "help and tips",
        "blog": "blog",
    },
    "permissions-overlay": {
        "all-roles": "all roles",
        "owner": "owner",
        "maintainer": "maintainer",
        "member": "member",
        "observer": "observer",
    },
    "onboarding": {
        "continue": "Continue",
        "back": "Back",
        "about-you": {
            "full-name": "Full name",
            "title": "About you",
            "prompt": "Write your full name below.",
        },
        "billing-details": {
            "title": "Billing details",
            "continue": "Continue to checkout",
            "continue-message":
                "We use Stripe for our payment processing services.",
        },
        "payment-error": {
            title: "Please finish setting up your billing account",
            continue: "Return to checkout",
            prompt: [
                "Your free 31 day trial has not begun yet.",
                "Your workspace does not yet have seats assigned to it.",
                "Please return to Stripe to finish the checkout process.",
            ],
        },
        "new-section": {
            title: "We’ve put your task in a ‘To do’ section.",
        },
        "new-workspace": {
            "title": "Let’s set up your first workspace, {who}.",
            "prompt": "You can create and manage numerous workspaces",
            "has-workspace":
                "It looks like you already have a workspace, would you like to create a workspace board?",
            "placeholder": "e.g. the name of your company",
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
            "cancel": "Cancel",
            "workspace-board-exists": {
                message:
                    'It looks like you already have a workspace board called "{title}". Would you like to continue adding a task for it?',
                prompt: 'Continue adding task to "{title}"',
            },
        },
        "new-task": {
            "title": "What is a task you’d like to complete?",
            "workspace-board-section-title": "To do",
            "prompt": {
                location:
                    'This task will be placed in a section called "{workspaceBoardSectionTitle}"',
                exists: 'It looks like you already have a workspace board section called "{workspaceBoardSectionTitle}". We will now create a task  and place it into that workspace board section.',
                explanation:
                    "Tasks can be further divided into sub tasks and contain detailed descriptions.",
            },
            "placeholder": "E.g., 'Add user permission dropdown'",
        },
        "new-label": {
            title: 'Create a label for "{taskTitle}"',
            prompt: "Labels help you to filter between the types of tasks.",
            placeholder: "e.g., Bug",
        },
        "assign-task": {
            title: 'Task "{taskTitle}" has been assigned to you!',
            continue: "Get started",
            prompt: {
                "finished": "You’re all set!",
                "adding-workspace-users":
                    "If you wish to add new workspace users to your workspace, please go to the workspace settings menu next to your workspace name.",
            },
        },
    },
    "auth": {
        "sign-up": {
            "title": "Sign up",
            "sub-title": "Sign up and start a free trial",
            "enter-your-email": "Enter your email",
            "email": "Email",
            "enter-your-password": "Enter your password",
            "password": "Password",
            "tos-privacy": {
                "i-agree": "I agree to the",
                "terms": "Terms of Service",
                "and": "and",
                "privacy-statement": "Privacy Statement",
            },
            "sign-up": "Sign up",
            "already-have-an-account": "Already have an account?",
            "invalid-credentials":
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
    },
    "log-in": {
        "title": "Log in",
        "enter-your-email": "Enter your email",
        "email": "Email",
        "enter-your-password": "Enter your password",
        "password": "Password",
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
        "enter-your-email": "Enter your email",
        "email": "Email",
        "send-reset-password-link": "Send reset password link",
        "return-to-log-in": "Return to log in",
    },
    "confirm-password-reset": {
        "title": "Reset your password",
        "enter-new-password": "Enter new password",
        "new-password": "New password",
        "confirm-new-password": "Confirm new password",
        "reset-password": "Reset password",
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
            "empty-state":
                "You have not added any sub tasks yet. You can add a sub task by clicking the add sub task button.",
            "empty-state-read-only":
                "This task has no sub tasks. You can add sub tasks by going to the task edit screen and clicking the add sub task button from there.",
            "add-sub-task": "Add sub task",
        },
        "new-task-breadcrumb": "New task (currently creating)",
        "new-task-name": "New task name",
        "description": "Description",
        "labels": "Labels",
        "section": "Section",
        "select-due-date": "Select due date",
        "no-due-date": "No due date",
        "due-date": "Due date",
        "edit": "Edit",
        "task-title": "Task title",
        "assignee": "Assignee",
        "enter-a-subtask": "Enter a subtask",
        "due-soon": "Due soon!",
    },
    "user-account-settings": {
        "title": "User account settings",
        "overview": {
            "full-name": {
                label: "Full name",
                placeholder: "Enter your full name",
            },
            "profile-picture": {
                prompt: "Upload a profile picture",
                current: "Your current profile picture",
            },
            "your-current-avatar": "Your current avatar",
            "update-email": "Update email address",
            "change-password": "Change password",
            "delete-account": "Delete account",
            "cancel": "Go back",
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
    "404": "404",
    "home": "Home",
    "signout": "Signout",
    "signup": "Signup",
    "signin": "Signin",
    "welcome-home": "Welcome Home",
    "sign-up-cta": "Sign up",
    "page.signup.msg": "Let's set up your account, Already have one?",
    "sign-in-here": "Sign in here.",
    "email": "Email",
    "please-enter-your-email": "Please enter your email",
    "password": "Password",
    "please-enter-a-password": "Please enter a password",
    "user-already-exist": "User already exist.",
    "signup-privacy":
        "I accept the Projectify Terms of Service. For more information about Projectify's use and protection of your data, please see our Privacy Policy.",
    "email-sent": "Email sent",
    "i-sent-an-email-to": "I sent an email to",
    "please-proceed-from-the-url-described-in-the-message":
        "Please proceed from the url described in the message.",
    "top-page": "Top page",
    "password-reset": "Password reset",
    "user-not-found": "User not found.",
    "send": "Send",
    "password-reset-email-sent": "Password reset email sent",
    "please-enter-your-email-to-request-a-password-reset":
        "Please enter your email to request a password reset.",
    "password-can-not-be-empty": "Password can not be empty.",
    "something-went-wrong": "Something went wrong.",
    "password-reset-complete": "Password reset complete",
    "user-password-reset-completed-msg":
        "Your password has been changed. Please log in to continue using Projectify.",
    "loading": "Loading...",
    "error": "Error",
    "sign-in": "Sign in",
    "lets-set-up-your-account-dont-have-one-yet":
        "Let's set up your account, Don't have one yet?",
    "sign-up-here": "Sign up here.",
    "wrong-email-or-password": "Wrong email or password.",
    "forget-password-password-reset": "Forget password? Password reset",
    "here": "here.",
    "task-name": "Task Name",
    "save": "Save",
    "task": "Task",
    "discussion": "Discussion",
    "description": "description",
    "please-enter-a-description": "Please enter a description",
    "sub-task": "Sub Task",
    "new-sub-task-name": "New sub task name",
    "section-title": "Section Title",
    "title": "title",
    "create": "Create",
    "board-name": "Board name",
    "deadline": "Deadline",
    "new-section": "New Section",
    "new-task": "New task",
    "Edit": "Edit",
    "Archive": "Archive",
    "Delete": "Delete",
    "Cancel": "Cancel",
    "Confirm": "Confirm",
    "deleted-section-cannot-be-returned-would-you-like-to-delete-this-section":
        "Deleted section cannot be returned. Would you like to delete this section ?",
    "delete-section": "Delete Section",
    "Save": "Save",
    "please-enter-a": "Please enter a",
    "workspace-board-name": "workspace board name",
    "archive-board-message":
        "Would you like to archive this board? You can see archived boards in archives screen.",
    "delete-board-message": "Would you like to delete this board?",
    "archive-board": "Archive Board",
    "delete-board": "Delete Board",
    "section-name": "section name",
    "delete-task-modal-message":
        "Deleted task cannot be returned. Would you like to delete this task?",
    "delete-task": "Delete Task",
    "remove-section-tooltip-message":
        "You need to remove all tasks in order to delete this section",
    "edit-section": "Edit Section",
    "logout": "Logout",
    "workspace-settings": {
        "title": "Workspace settings",
        "tab-bar": {
            "general": "General",
            "workspace-users": "Workspace users",
            "billing": "Billing",
        },
        "general": {
            "title": "General",
            "save": "Save",
            "delete": "Delete workspace",
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
            },
        },
        "workspace-users": {
            "title": "Workspace users",
            "search": {
                label: "Search workspace users",
                placeholder: "Enter a query to search for workspace users",
            },
            "search-workspace-users": "Search workspace users",
            "no-job-title": "No job title",
            "no-workspace-users-found":
                "No workspace users found for this search query. Please try another search.",
            "role": "Role",
            "workspace-user-details": "Workspace user details",
            "invite-new-workspace-users": "Invite new workspace users",
        },
        "billing": {
            "title": "Billing",
            "current-plan": "Current plan",
            "monthly-total": "Monthly total ($8 per seat/month):",
            "edit-billing-details": "Edit billing details",
            "contact-us-to-request-changes":
                "Contact us to request changes to your plan",
            "billing-contact": "hello@projectifyapp.com",
            "seats": {
                "number-of-seats": "Number of seats:",
                "format":
                    "{seats} ({seats_remaining} {seats_remaining, plural, one {seat} other {seats}} remaining)",
            },
        },
    },
    "my-profile": "My Profile",
    "remove": "Remove",
    "new-workspace-user": "New workspace user",
    "no-archived-boards-found": "No archived boards found.",
    "new-label": "Create New Label",
    "delete-label": "Delete label",
    "are-you-sure-you-want-to-delete-this-label":
        "Are you sure you want to delete this label?",
    "create-new-label": "Create new label",
    "name": "Name",
    "please-enter-a-label-name": "Please enter a label name.",
    "color": "Color",
    "please-enter-a-label-color": "Please enter a label color.",
    "edit-label": "Edit label",
    "this-field-is-required": "This field is required",
    "general": "General",
    "labels": "Labels",
    "select-date": "Select date",
    "apply-labels": "Apply labels",
    "disconnected-network": "Disconnected Network",
    "back-to-landing-page": "back to landing page",
    "layout": "Layout",
    "filter-tasks": "Filter tasks",
    "tasks-not-found-for": "Tasks not found for",
    "clear-labels-filter": "Clear labels filter",
    "filter-by-labels": "Filter by labels",
    "search": "Search",
    "clear-selection": "Clear Selection",
    "select-me": "Select Me",
    "page-not-found": "Page not found",
    "the-page-you-are-looking-for-could-not-be-found":
        "the page you are looking for could not be found.",
    "go-back": "Go Back",
    "enable-smooth-project-management": "Enable smooth project management.",
    "service": "Service",
    "support": "Support",
    "policy": "Policy",
    "terms": "Terms",
    "company": "Company",
    "about": "About",
    "blog": "Blog",
    "contact": "Contact",
    "legal": "Legal",
    "social": "Social",
    "go-to-homepage": "Go to homepage",
    "workspace-not-found": "Workspace not found",
    "retun-to-dashboard": "Retun to dashboard",
    "board-not-found": "Board not found",
    "task-not-found": "Task not found",
    "this-application-is-best-used-on-a-pc":
        "This application is best used on a PC",
    "Problem": "Problem",
    "Solution": "Solution",
    "Github": "Github",
    "auto-system-preference": "Auto (System preference)",
    "light": "Light",
    "dark": "Dark",
    "appearance": "Appearance",
    "assigned-to-nobody": "Assigned to nobody",
    "updates": "Updates",
    "open-task": "Open task",
    "move-to-section": "Move to section",
    "move-to-top": "Move to top",
    "move-to-bottom": "Move to bottom",
    "move-to-previous-position": "Move to previous position",
    "move-to-next-position": "Move to next position",
    "copy-link": "Copy link",
    "goto-to-updates": "Goto to updates",
    "expand-section": "Expand section",
    "collapse-section": "Collapse section",
    "switch-with-previous-section": "Switch with previous section",
    "switch-with-next-section": "Switch with next section",
    "add-task": "Add Task",
    "product": "Product",
    "features": "Features",
    "solutions": "Solutions",
    "pricing": "Pricing",
    "help-and-tips": "Help and tips",
    "resources": "Resources",
    "about-us": "About us",
    "careers": "Careers",
    "accessibility-statement": "Accessibility statement",
    "contact-us": "Contact us",
    "privacy": "Privacy",
    "project-management-at-pace": "Project management at pace.",
    "start-a-free-trial": "Start a free trial",
    "edit-labels": "Edit labels",
    "expand-sidebar": "Expand sidebar",
    "minimise-sidebar": "Minimise sidebar",
    "continue-to-dashboard": "Continue to dashboard",
    "log-in-cta": "Log in",
    "add-label": "Add label",
    "role": "Role",
    "edit-remove": "Edit/remove",
    "name-0": "name",
    "email-0": "email",
    "job-title": "job title",
    "permissions": "permissions",
    "selecat-a-permission": "selecat a permission",
    "all-roles": "All roles",
    "you-have-seats-seats-left-in-your-plan":
        "You have {seats} seats left in your plan",
    "you-have-0-seats-left-in-your-plan": "You have 0 seats left in your plan",
    "location": "Location",
    "index": {
        "hero-header": "Manage projects the right way.",
        "hero-text":
            "Warp drive your way to success with software that helps you to collaborate on and manage projects efficiently, with speed.",
        "hero-button": "Start a free trial",
        "hero-alt":
            "An illustration showing the look and feel of tasks in Projectify's user interface",
        "trust-header-1": "Everything you need to",
        "trust-header-2": "stay organised",
        "trust-header-3": "and",
        "trust-header-4": "deliver faster",
        "trust-text": "The go-to project management tool for developers.",
        "feature-1-header":
            "Task cards that are accessible and keyboard friendly",
        "feature-1-text":
            "No more drag and drop disasters! Create and move tasks around the board with ease and speed. Organise and prioritize your workload with peace of mind.",
        "feature-2-header":
            "Transform mammoth tasks into smaller, feasible ones",
        "feature-2-text":
            "Sub tasks break up the workload to allow for large tasks and progress to become more realistic and achievable. Add, reorder, edit and delete limitless sub tasks.",
        "feature-3-header": "Full control of your workspaces",
        "feature-3-text":
            "List and column views allow you to organise workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, users or keyboards to focus on specific tasks.",
        "feature-4-header": "Keep an eye on important updates",
        "feature-4-text":
            "Whether its a question about a task, a change of assignee or simply a task moving to the next stage of development, notifications immediately let you know when there's an update.",
        "feature-5-header": "Responsive for on-the-go",
        "feature-5-text":
            "Need to access your projects whilst away from the office? No app. No problem. A fully responsive experience to stay connected and keep projects on track.",
        "feature-6-header": "We never sell your data. Ever.",
        "feature-6-text":
            "Our platform full complies with GDPR regulations, amongst others, so you can be rest assured that your private information, stays private.",
        "feature-7-header": "Projectify is 100% open source software",
        "feature-7-text-1":
            "We believe in transparency and being developer friendly, which is why our source code can be found online.",
        "solution-header": "Meeting diverse needs with practical solutions.",
        "solution-subtitle":
            "From companies big and small to individuals working alone, Projectify can be used to manage all kinds of tasks.",
        "solution-1": "Development teams",
        "solution-2": "Research",
        "solution-3": "Project management",
        "solution-more": "See more use cases",
    },
    "pricing-page": {
        "header": "Pricing",
        "subtitle": "One plan. One price. All features.",
        "plan": "Universal Plan",
        "price": "$8",
        "seat-per-month": {
            seat: "seat",
            per: "/",
            month: "month",
        },
        "feature-title": "What's included?",
        "feature-1": "Unlimited tasks",
        "feature-2": "Unlimited boards",
        "feature-3": "Unlimited update logs",
        "feature-4": "Collaborate with workspace users",
        "feature-5": "Add multiple labels",
        "feature-6": "Role permissions",
        "feature-7": "Set due dates",
        "feature-8": "Customise your workspace",
        "feature-9": "Archive completed boards",
        "feature-10": "Real time notifications",
        "feature-11": "File storage of 3 GB",
        "feature-12": "Filter by label or assignee",
        "feature-13": "Accessible interface",
        "feature-14": "Open source software",
        "join": "Join the members already using Projectify to manage their projects",
        "card-figure-1": "2500+",
        "card-description-1": "Tasks created on Projectify",
        "card-figure-2": "250+",
        "card-description-2": "Labels applied on Projectify",
        "card-figure-3": "200+",
        "card-description-3": "Boards created on Projectify",
    },
    "solutions-page": {
        "hero-header": "Solutions for every type of user",
        "hero-text":
            "Explore the different ways users are using Projectify to meet deadlines, reach targets and be productive.",
        "developer": "Development teams",
        "dev-description":
            "Monitor team progress throughout the whole software lifecyle.",
        "project-management": "Project management",
        "project-description":
            "Faciliate rapid delivery across multiple projects for any industry.",
        "research": "Research",
        "research-description":
            "Keep track of testing processes and results with incredible detail.",
        "remote": "Remote work",
        "remote-description":
            "Asynchronous communication whether you're at home or away.",
        "academic": "Academic endeavours",
        "academic-description":
            "Structure a thesis, organise a project or keep track of assignments.",
        "personal-use": "Personal use",
        "personal-description":
            "Log an exercise routine, create a new diet or plan an adventure. The possibilities are endless.",
        "more": "Learn more",
    },
    "development-solutions": {
        "hero-header": "Development solutions",
        "hero-text":
            "How development teams can use Projectify to create tasks, monitor pulls requests and deploy faster.",
        "feature-1-header": "Organise with labels and task numbers",
        "feature-1-text":
            "Use labels with terms like bug, enhancement or backend to categorize tasks. Filter with labels or search by task number to quickly locate what you're looking for.",
        "feature-2-header": "Live notifications",
        "feature-2-text":
            "Notifications provide you with all the information you need whilst also giving you conveniant 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
        "feature-3-header": "Plan and execute",
        "feature-3-text":
            "Set up and monitor pull requests, merges, bug fixes and more for multiple workspace users of your team.",
    },
    "research-solutions": {
        "hero-header": "Research solutions",
        "hero-text":
            "How researchers teams can use Projectify to collaborate on data with colleagues and meticulously catalogue findings.",
        "feature-1-header": "Catergorize data with labels and numbers",
        "feature-1-text":
            "Labels simplify the process of categorizing tasks. Automatically assigned task numbers take organisation one step further",
        "feature-2-header": "Provide and request updates on any task",
        "feature-2-text":
            "The updates sections allows you and your colleagues to share new details about how a test, experiment or study has gone.",
        "feature-3-header": "Create and monitor multiple projects",
        "feature-3-text":
            "With unlimited project boards and tasks per workspace, you're free to perform as much research and testing as you require.",
    },
    "project-solutions": {
        "hero-header": "Project management solutions",
        "hero-text":
            "How project managers can use Projectify to efficiently manage tasks, projects and workspace users of their team.",
        "feature-1-header": "An ethical approach to management",
        "feature-1-text":
            "View how many tasks a workspace user has assigned to them, so the workload can be divided equally. Filter by workspace user to see what individual colleagues are working on.",
        "feature-2-header": "Live notifications",
        "feature-2-text":
            "Notifications provide you with all the information you need whilst also giving you conveniant 'reply' and 'go to task' actions. The notification center houses updates from all workspaces so you never miss a beat.",
        "feature-3-header": "Full control of your workspaces",
        "feature-3-text":
            "List and column views allow you to organise workflows and see the bigger picture. Split your workspace into boards to enable multi-project management. Filter by labels, users or keyboards to focus on specific tasks.",
        "feature-4-header": "Permissions to control access",
        "feature-4-text":
            "Make sure nothing important gets deleted. With permission roles - Owner, Maintainer, Member and Observer, you can be safe in knowing there won't be any accidentally data loss.",
    },
    "academic-solutions": {
        "hero-header": "Academic solutions",
        "hero-text":
            "How students can use Projectify to plan a thesis, collaborate, or keep track of assignments.",
        "feature-1-header": "Deadlines become a lifeline",
        "feature-1-text":
            "Projectify notifies you of upcoming due dates for assignments, so you'll never miss a paper's deadline.",
        "feature-2-header": "Checklists that aid your progress",
        "feature-2-text":
            "We know that projects and dissertations can be daunting, but we're here to help. Breaking tasks into smaller sub tasks allow you to micro-achieve your way to completion.",
        "feature-3-header":
            "Create notes on each task and coordinate with friends",
        "feature-3-text":
            "Invite friends and classmates into your workspace to collaborate, share ideas and more.",
    },
    "remote-solutions": {
        "hero-header": "Remote solutions",
        "hero-text":
            "How remote workers can use Projectify to keep in tune with projects and stay connected.",
        "feature-1-header": "Work together across timezones",
        "feature-1-text":
            "Asynchronous communication is vital for all teams be they remote or in the office. Assign tasks, create new projects and provide updates, anywhere, anytime.",
        "feature-2-header": "Notifications and updates on any task",
        "feature-2-text":
            "Notifications allow for important information to be delivered, even if you're not around. When you're away from your computer, updates to task will stay unread in the notification center until you get back.",
        "feature-3-header": "Assign tasks to users all over the world",
        "feature-3-text":
            "Whether it's Leo in the Phillipines or Valerie in Brazil, once you assign a task to someone they will be notified immediately with a pop-up.",
    },
    "personal-solutions": {
        "hero-header": "Personal solutions",
        "hero-text":
            "How people can use Projectify for everyday life, whether it be keeping track fo your health or creating an itinerary for a trip.",
        "feature-1-header": "Create tasks with ease",
        "feature-1-text":
            "Organise your tasks into individual projects with sections such as 'To do', 'In progress' and 'Done'. Provide descriptions for each task and set deadlines. Labels simplify the process of catergorizing tasks.",
        "feature-2-header": "Check off sub tasks as you go",
        "feature-2-text":
            "Need to plan an event? Want to create a list of achievements? Sub tasks help you to check off small tasks bit by bite.",
        "feature-3-header": "Add friends and family to your space",
        "feature-3-text":
            "Get everyone on the same page by assigning task to different workspace users.",
    },
    "accessibility": {
        "hero-header": "Accessibility statement",
        "a-goals": "Accessibility goals",
        "a-goals-text":
            "Projectify is committed to ensuring digital inclusivity and accessibility for people with diverse disabilities. We are continually improving the user experience for everyone, and applying the relevant accessibility standards. We are also aiming to improve the use of both our website and platform for members who employ assistive technologies.",
        "a-measures": "Measures we take to support accessiblity",
        "a-measures-list-1":
            "Include accessibility as part of our mission statement",
        "a-measures-list-2":
            "Ensure designs meet a minimum accessibilty level (WCAG 2.1 level AA)",
        "a-measures-list-3":
            "Compatibility with different web browsers and assistive technology",
        "a-measures-list-4":
            "Include people with disabilities in our user personas",
        "a-measures-list-5":
            "Conduct usability tests with people who have disabilities",
        "a-conformance": "Conformance status",
        "a-conformance-text":
            "The Web Content Accessibility Guidelines (WCAG) standard defines requirements to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA. 'Fully conforms' means that the content meets all of the WCAG requirements at the specified Level without exceptions. Although our goal is WCAG 2.1 Level AA conformance, we have also applied some Level AAA Success Criteria: Images of text are only used for decorative purposes. Content posted since May 2022 fully conforms to WCAG 2.1 Level AA. It partially conforms to Level AAA.Older content conforms to earlier versions of WCAG, for example, WCAG 2.0.",
        "a-compatibility":
            "Compatibility with browsers and assistive technologies",
        "a-compatibility-text":
            "The Projectify website and platform is designed to be compatible with assistive technologies and the last two versions of major browsers. The website and platform are not designed for Internet Explorer 11 and earlier versions.",
        "a-platform": "Platform",
        "a-platform-text":
            "We are currently in the process of making our platform conform to accessiblity standards. Our main focus is to improve color contrast in both the light and dark modes of our platform, increase discoverability of features for users with vision impairments and enhance the usability of our main components.",
        "a-website": "Website",
        "a-website-list-1":
            "Keyboard navigation: All menus, buttons , inputs and actions are accessible from a keyboard",
        "a-website-list-2":
            "Screen reader compatibility: Our code supports the use of screen readers for users who digest information through audio means",
        "a-website-list-3":
            "Images: All images are supported with descriptive and accurate alternative text which can be read by screen readers",
        "a-website-list-4":
            "Text: Our text size, weight and font style have been carefully chosen to be accessible to members with dyslexia and/or visual impairment. WCAG 2.0 level AA requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text.",
        "a-website-list-5":
            "Color: WCAG 2.1 requires a contrast ratio of at least 3:1 for graphics and user interface components, which we meet",
        "a-website-list-6":
            "Magnification: For sight impaired users, all pages and content can be magnified using standard browser controls or magnification software",
        "a-limitations": "Limitations",
        "a-limitations-text":
            "We are aware that, despite our best efforts, there may be limitations to the accessibilty of both the platform and website. Below is a description of known limitations. Please contact us if you discover an issue not listed below. Known limitations of the platform:",
        "a-limitations-list-1":
            "Tab selection not working on the calendar menu",
        "a-limitations-list-2":
            "Not all screen readers can read placeholder text",
        "a-evaluation": "Evaluation report",
        "a-evaluation-text":
            "An evaluation report can be found here link. Assessment of both the platform and website was carried out by self-evaluation.",
        "a-contact": "Contact us",
        "a-contact-text":
            "We welcome feedback on the accessibility of Projectify. If you encounter any acccessibility barriers whilst using the platform or website, please email hello@projectify.com. ",
    },
    "help": {
        "hero-header": "Help and tips",
        "hero-text": "Learn to fly through projects with speed and agility",
        "help-sections": "Help sections",
        "basics": "Basics",
        "workspaces": "Workspaces",
        "boards": "Boards",
        "sections": "Sections",
        "tasks": "Tasks",
        "labels": "Labels",
        "workspace-users": "Workspace users",
        "bulk-select": "Bulk select",
        "filters": "Filters",
        "notifications": "Notifications",
        "pop-ups": "Pop ups",
        "billing": "Billing and accounts",
        "skip": "Skip ahead to",
    },
    "help-basics": {
        "workspace": "What is a workspace?",
        "workspace-text":
            "A workspace is an area where you can create projects, tasks, labels and invite various members of your organisation as workspace users. In a workspace you can set permissions and customise the overall look and feel of your productivity center. For more information on workspaces please see Workspaces.",
        "board": "What is a board?",
        "board-text":
            "A board is a specific project in your workspace that you would like to work on.You can create unlimited boards per workspace and have the freedom to rename and organise them.Completed boards can be archived to remove clutter from your workspace. For more information on boards please see Boards.",
        "section": "What is a section?",
        "section-text":
            "A section is a category that you can divide tasks into. Popular categories include ‘To do’ ‘In progress’ and ‘Done’. Sections can be moved and edited freely. For more information on sections please see Sections.",
        "task": "What is a task?",
        "task-text":
            "A task is a step in your project that needs to be completed. Tasks can be assigned to any member in your workspace. Labels and detailed information can be applied to tasks. For every task that is created, a unique task number is assigned to it for ease of reference and searching. Tasks can be further divided into sub tasks - sub tasks are great for keeping track of micro achievements per task. Due dates can also be set for tasks that need to be completed on a deadline.For more information on tasks please see Tasks.",
        "side-menu": "How to use the side menu",
        "side-menu-text":
            "The side menu allows for full control of your workspace and projects.You are able to switch between workspaces or boards through this menu. Filtering between workspace users and labels can also be performed here.Workspace settings such as permissions and billing can be accessed from this menu.The menu can be viewed in full expanded mode or in collapsed mode.",
    },
    "help-workspaces": {
        "create": "Create a workspace",
        "create-text": "/",
        "switch": "Switch workspaces",
        "switch-text": "/",
        "settings": "Workspace settings",
        "settings-text": "/",
        "delete": "Delete a workspace",
        "delete-text": "/",
    },
    "help-boards": {
        "create": "Create a board",
        "create-text": "/",
        "edit": "Edit a board",
        "edit-text": "/",
        "archive": "Archive a board",
        "archive-text": "/",
        "delete": "Delete a board",
        "delete-text": "/",
        "overview": "Board overview",
        "overview-text": "/",
    },
    "help-sections": {
        "create": "Create a section",
        "create-text": "/",
        "nav": "Section navigation",
        "nav-text": "/?",
        "sub-menu": "Section sub-menu",
        "sub-menu-text": "/",
        "move": "Move a section",
        "move-text": "/",
        "edit": "Edit a section",
        "edit-text": "/",
        "delete": "Delete a section",
        "delete-text": "/",
    },
    "help-tasks": {
        "create": "Create a task",
        "create-text": "/",
        "context": "Add context to your task",
        "context-text": "/",
        "edit": "Edit a task",
        "edit-text": "/",
        "move": "Move a task",
        "move-text": "/",
        "delete": "Delete a task",
        "delete-text": "/",
    },
    "help-labels": {
        "create": "Create a label",
        "create-text": "/",
        "apply": "Apply a label to a task",
        "apply-text": "/",
        "edit": "Edit a label",
        "edit-text": "/",
        "filter": "Filter by labels",
        "filter-text": "/",
        "delete": "Delete a lable",
        "delete-text": "/",
        "ways": "Ways to use labels",
        "ways-text": "/",
    },
    "help-workspace-users": {
        "invite": "Invite a workspace user",
        "invite-text": "/",
        "assign": "Assign a task to a workspace user",
        "assign-text": "/",
        "filter": "Filter by workspace user",
        "filter-text": "/",
        "edit": "Edit workspace user permissions",
        "edit-text": "/",
        "delete": "Delete a workspace user",
        "delete-text": "/",
    },
    "help-bulk": {
        "activate": "How to activate bulk select",
        "activate-text": "/",
        "move": "Bulk move",
        "move-text": "/",
        "assign": "Bulk assign/reassign",
        "assign-text": "/",
        "delete": "Bulk delete",
        "delete-text": "/",
    },
    "help-filters": {
        "workspace-user": "Filter and search by workspace user",
        "workspace-user-text": "/",
        "label": "Filter and search by label",
        "label-text": "/",
        "keyword": "Search by keyword",
        "keyword-text": "/",
        "ways": "Ways to use filters",
        "ways-text": "/",
    },
    "help-notifications": {
        "center": "The notification center",
        "center-text": "/",
        "card": "The notification card",
        "card-text": "/",
        "types": "Types of notifications",
        "types-text": "/",
        "actions": "Perform actions on notifications",
        "actions-text": "/",
    },
    "help-pop-ups": {
        "types": "Types of pop-up",
        "types-text": "/",
        "actions": "Perform actions on pop-ups",
        "actions-text": "/",
    },
    "help-billing": {
        "settings": "Billing settings",
        "settings-text":
            "To go to workspace settings, click the ellipsis next to the workspace button in the side menu. This will open up a sub menu where you can access the current workspace’s settings page. From this page, you can access the billing settings of your account.",
        "workspace": "Removing/adding workspaces",
        "workspace-text":
            "Only users with the permission role of Owner can create and delete workspaces. You will need to provide your banking details for each workspace you create.",
        "workspace-users": "Removing/adding workspace users",
        "workspace-users-text":
            "Only users with the permission role of Owner can invite or remove users. Be aware that you will not be able to invite workspace users if you do not have enough seats available in your workspace. In order to add more seats, please amend the seat numbers in your account.",
        "delete": "Delete your account",
        "delete-text":
            "To delete your account visit the billing page in workspace settings and cancel your subscription. Deleting your account will also remove workspace users from any workspaces that you own.You can transfer ownership of the account to a different workspace user before deletion to ensure that content and workspace users can continue to use the workspace. Deleting your account without transferring ownership will delete all data including personal information and all content created on the platform will cease to exist.",
    },
    "header": {
        "features": "Features",
        "solutions": "Solutions",
        "help": "Help",
        "company": "Company",
        "pricing": "Pricing",
        "log-in": "Log in",
        "start-a-free-trial": "Start a free trial",
        "continue-to-dashboard": "Continue to dashboard",
        "skip": "Skip",
    },
};
export default messages;
