<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Security

This page explains measures taken by JWP Consulting GK (hereinafter referred to
as "JWP") to ensure the security of the Projectify software (hereinafter
referred to as "Projectify"). JWP offers Projectify to users as defined in
the [terms of service](/tos) and those who are interested in using Projectify
(both hereinafter referred to as "you") .

This page contains a security assessment created following the [Minimum Viable
Secure Product checklist v2.0](https://mvsp.dev/mvsp.en/v2.0-20221012/). JWP
invites you to [share your feedback](/contact-us). For security related
inquiries, please refer to the [security disclosure policy](/security/disclose).

# Version history

| Date           | Changes                                           | Author                                |
| -------------- | ------------------------------------------------- | ------------------------------------- |
| **2026-04-11** | Edited to reflect Hetzner migration | Justus W. Perlwitz, JWP Consulting GK |
| **2026-02-20** | Adjusted content based on Django frontend rewrite | Justus W. Perlwitz, JWP Consulting GK |
| **2024-03-29** | Created page                                      | Justus W. Perlwitz, JWP Consulting GK |

# Business controls

JWP offers a point of contact for Projectify-related vulnerability reports on
Projectify's [security disclosure policy page](/security/disclose).

If you would like to evaluate the security of Projectify, JWP offers dedicated
test environments. Please [contact JWP](/contact-us) for more details.

JWP has **not** commissioned external penetration testing of Projectify as of
2024-03-29.

JWP trains its personnel in information security and stays up to date with
threats. JWP follows industry standards to securely design, implement, and operate Projectify.

## Compliance

JWP offers Projectify in compliance with [Japanese and EU (GDPR) privacy
regulations](/privacy). To use Projectify, you have to agree with its
[terms of service](/tos).

Please [reach out](/contact-us) if you have any compliance related inquiries.

## Incident handling

When a security incident on Projectify affects you, JWP will contact you no later
than 72 hours with the following information:

- How you are affected
- Preliminary technical analysis of the breach
- Remediation plan with reasonable timelines
- Point of contact for your inquiries

## Data handling

JWP does not store your data on its own premises. All third parties handling
user data follow
data sanitization best practices.

# Application design controls

Projectify does not implement Single Sign-On (SSO).

You can only use Projectify using HTTPS. Projectify redirects HTTP connections to
`www.projectifyapp.com` to the corresponding HTTPS address. Example:

`http://www.projectifyapp.com/dashboard` becomes `https://www.projectifyap.com/dashboard`.

Projectify uses the following HSTS policy:

```
strict-transport-security max-age=31536000
```

Projectify does not use HSTS preloading. [^hsts]

[^hsts]: [HSTS Preload List Submission](https://hstspreload.org/) _hstspreload.org_

Projectify uses the following Content Security Policy[^csp]:

```
script-src 'self'
```

[^csp]: [Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) _developer.mozilla.org_

To prevent `iframe` embedding, Projectify sets the `X-Frame-Options` HTTP
response header to `DENY`.

## Password policy

Projectify's Django backend stores your password in a secure form by hashing it with a salt using PBKDF2 with SHA256[^django-passwords]. You can use passwords containg up to 128 characters. Your browser transmits your password to Projectify over an encrypted connection (HTTPS) when you set your password or log in.

Projectify never stores or log your password in plain text.

To change your password, you must provide your old password. Projectify
sends you a confirmation mail when your password changes.

To reset your password, you can request a password reset. When you request a password reset, Projectify sends you a reset confirmation email.
Clicking the reset link inside the email lets you set a new password and finish
the password reset process. Projectify sends you a confirmation mail when your
password resets.

Projectify does not use secret questions for logging in or resetting passwords.

Projectify prevents password brute-forcing, dictionary attacks, and credential
stuffing by limiting the number of failed log-in attempts
that someone can perform in a given amount
of time.

Projectify enforces password policies that prevent users from using weak and
easy to guess
passwords.

[^django-passwords]: ["By default, Django uses the PBKDF2 algorithm with a SHA256 hash, a password stretching mechanism recommended by NIST."](https://docs.djangoproject.com/en/6.0/topics/auth/passwords/#how-django-stores-passwords) _docs.djangoproject.com_

## Dependency patching

JWP keeps Projectify's third dependencies up to date and responds to known
vulnerabilities.
JWP uses Dependabot [^dependabot] to monitor new vulnerabilities in Projectify's
source code repository [^repository].

[^dependabot]: [About Dependabot](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart-guide#about-dependabot) _docs.github.com_
[^repository]: [Projectify source code repository](https://github.com/jwpconsulting/projectify) _github.com/jwpconsulting/projectify_

## Logging

To help you understand how someone accessed your account, Projectify logs the following information:

- Last time of successful log-in

Projectify does **not** log the following information:

- Users logging in and out
- Read, write, delete operations on application and system users and objects
- Security settings changes (including disabling logging)
- Application owner access to customer data (access transparency)

## Encryption

We've taken specific measures to protect your sensitive data
in transit and in storage.

### Application and database server

Projectify uses TLS for the following connections:

- When your browser connects to Projectify
- Sending mails with Lettermint, see [Transactional mailing](#transactional-mailing)

### Database

Projectify's database server does not encrypt its data at rest.
Hetzner encrypts managed server backups at rest.[^confidentiality]

### Asset storage

Projectify stores media files on the same server that the backend and
PostgreSQL database server run on.

This data is not encrypted at rest.[^confidentiality]

[^confidentiality]: See "Encryption of Data (at rest)" and "Encryption
of Backups (at rest)" at <https://docs.hetzner.com/general/security-and-identify/technical-and-organizational-measures#confidentiality>

### Transactional mailing

Projectify uses the transactional mailing service Lettermint
to send you emails. Lettermint's Trust Center does not mention whether they
store emails encrypted at rest. [lettermint-trust-center].

[^lettermint-trust-center]: [Lettermint Trust Center](https://trust.lettermint.co/) *trust.lettermint.co*

# Application implementation controls

## List of data

Please review the [privacy policy](/privacy) for a detailed listing of sensitive
data handled by Projectify.

## Data flow diagram

Your browser connects to Projectify using the `www.projectifyapp.com` address
and
some user data flows from Projectify to various backend services. See the
following diagram:

```
.--------------.    .---------.   .------------------.
| Your Browser +----+ Backend +---+ Hetzner backups  |
.--------------.    .---+-----.   .------------------.
                        |
                        |         .------------.
                        .---------+ Lettermint |
                                  .------------.
```

## Vulnerability prevention and security libraries

To prevent vulnerabilities, Projectify contains the following measures:

- Projectify uses access controls to prevent users from accessing data or
  admin features that they are not authorized to.
- Projectify sends Session ID cookies over HTTPS only [^cookie-secure] and does
  not expose them to scripts. [^http-only]
- Projectify's Django backend prevents SQL injections in its ORM. [^django-sql]
  Projectify does not use raw SQL queries.
- Projectify's Django backend prevents cross-site scripting (XSS) by escaping untrusted inputs.
  [^django-xss]
- Projectify's Django backend prevents cross-site request forgery (CSRF) by checking for a `csrf`
  [^django-csrf]
  form attribute or HTTP header.

[^cookie-secure]: [Secure cookie configuration - `Secure`](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies#secure) _developer.mozilla.org_
[^http-only]: [Secure cookie configuration - `HttpOnly`](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies#httponly) _developer.mozilla.org_
[^django-sql]: [Security in Django - SQL injection protection](https://docs.djangoproject.com/en/6.0/topics/security/#sql-injection-protection) _docs.djangoproject.com_
[^django-xss]: [Security in Django - Cross site scripting (XSS) protection](https://docs.djangoproject.com/en/6.0/topics/security/#cross-site-scripting-xss-protection) _docs.djangoproject.com_
[^django-csrf]: [Security in Django - Cross site request forgery (CSRF) protection](https://docs.djangoproject.com/en/6.0/topics/security/#cross-site-request-forgery-csrf-protection) _docs.djangoproject.com_

## Time to fix vulnerabilities

JWP fixes any known exploitable vulnerabilities within 90 days of discovery.

## Build process

The build and deploy process is fully automated. Any dependencies used in the
Product are included in a reproducible way using Poetry lock files.

# Operational controls

## Physical access

All of Projectify's infrastructure is hosted by third parties which in turn
implement strict physical access controls.

## Logical access

Only Product administrators with a legitimate need have access to Projectify's
infrastructure or admin site.

Administrative accounts that are no longer needed are deactivated in a timely
manner.

JWP regularly reviews administrative accounts and only grants administrative
privileges to administrators where absolutely necessary.

Administrative access to Projectify's infrastructure is only possible using
Multi-Factor Authentication (MFA).

Administrative access to Projectify's admin site at
`www.projectifyapp.com/admin` is **not** secured by MFA.

## Subprocessors

A list of all subprocessors is available in the [GDPR section of the privacy
policy](/privacy) under **Article 6 (Cross-Border Data Transfer)**.

## Backup and disaster recovery

Projectify's PostgreSQL database creates hourly differential and
daily full backups of your data.

Projectify creates hourly backups of user generated media files.

Hetzner creates daily backups of all VPS storage drives used for Projectify.

The Projectify system logs any backup failures. There are no alerts for failing
backups.

**No** steps have been taken to periodically test backup restoration.

# Inquiries

Should you have any questions, please [reach out](/contact-us).
