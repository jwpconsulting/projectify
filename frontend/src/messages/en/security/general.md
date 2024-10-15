<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Security

This page explains measures taken by JWP Consulting GK (hereinafter referred to
as "we") to ensure the security of the Projectify software (hereinafter
referred to as the "Product"). The Product is offered to Users as defined in
the [terms of service](/tos) and those who are interested in using the Product
(both hereinafter referred to as "You") .

This page is a security-assessment created while reviewing the [Minimum Viable
Secure Product checklist v2.0](https://mvsp.dev/mvsp.en/v2.0-20221012/). We
invite You to share Your [feedback with us](/contact-us). For security related
inquiries, please refer to our [security disclosure
policy](/security/disclose).

# Version History

This page has been created on 2024-03-29.

# Business Controls

We offer a point of contact for vulnerability reports on our [security disclosure
policy page](/security/disclose).

If You would like to evaluate the security of the Product, We offer dedicated
test environments. Please [contact Us](/contact-us) for more details.

We have **not** commissioned external penetration testing of the Product as of
2024-03-29.

We train our personnel in information security. We stay up to date with
vulnerabilities and threats and securely design and implement the Product.

## Compliance

We offer the Product in compliance with Japanese and EU (GDPR) privacy
regulations, which You can [review here](/privacy). The Product is offered
according to the terms of service [found here](/tos).

Please [contact Us](/contact-us) for any other compliance inquiries.

## Incident handling

In the case of a security incident affecting You, we will inform You no later
than 72 hours with the following information:

- How You are affected
- Preliminary technical analysis of the breach
- Remediation plan with reasonable timelines
- Point of contact for Your inquiries

## Data handling

We have not implemented any specific measures for data handling.

# Application design controls

The Product does not implement Single Sign-On.

The Product can only be used using HTTPS. Any HTTP connection to the domains
www.projectifyapp.com and api.projectifyapp.com will be redirected to use
HTTPS. HSTS is used (strict-transport-security max-age=31536000). [HSTS
preloading](https://hstspreload.org/) is not used.

The Product's frontend at www.projectifyapp.com uses the following Content
Security Policy:

```
script-src 'self'
```

No specific measures for iframes have been taken.

## Password policy

PBKDF2 with SHA256 is used for password storage. There are no inherent limits
on password lengths in the backend. Since the password has to be transmitted
over HTTPS by a browser, fit into forms, and so on, we guarantee that passwords
up to 128 character are handled without any difficulties.

In order to reset Your password, We send a reset confirmation email to You.
The Product does not use secret questions for password resets. Confirming the
reset email is required to reset Your password.

To change Your password, You must provide Your old password. A confirmation
email is sent to You when Your password is changed.

**No** measures have been taken to prevent brute-forcing or credential
stuffing.

## Security libraries

User submitted data is sanitized in the backend by Django and Django Rest
Framework. Only translation data in the frontend is output as raw HTML,
everything else is escaped within the frontend's Svelte templates.

The Product is hardened against SQL injections as database access is handled by
Django's ORM.

## Dependency patching

We keep the Product's third dependencies up to date and respond to known
vulnerabilities. The Product's [GitHub
repository](https://github.com/jwpconsulting/projectify) enables Us to stay
informed of vulnerabilities by using
[Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot)

## Logging

We do **not** log the following information:

- Users logging in and out
- Read, write, delete operations on application and system users and objects
- Security settings changes (including disabling logging)
- Application owner access to customer data (access transparency)

## Encryption

Specific measures on our end have been taken to protect sensitive data in
transit between the Product's systems and in data storage and backups.

Apart from the frontend communicating with the backend using HTTPS, the
Product's systems use TLS for the following connections:

- Django backend to Redis Key-Value DB (Heroku Data for Redis)
- Django backend to PostgreSQL DBMS (Heroku Postgres)

For asset storage, it has **not** been verified whether the Cloudinary
(Cloudinary Inc.) APIs are accessed exclusively using a secure connection. It
is **not** known if Cloudinary uses encryption at rest. Cloudinary uses AWS S3
as a storage backend.

Heroku (Salesforce, Inc.) PostgreSQL storage and its backups are [encrypted at
rest](https://devcenter.heroku.com/articles/heroku-postgres-production-tier-technical-characterization#data-encryption).

Heroku Data for Redis does **not** use encryption at rest by itself. Some data
stored in Heroku Data for Redis is encrypted using symmetric encryption
(Django Channels messages). Other data is **not** encrypted using symmetric
encryption (Celery jobs).

It is **not** known what communication or at rest encryption the logging service
Papertrail (SolarWinds Worldwide, LLC) uses.

It is **not** known what communication or at rest encryption the APM service
New Relic (New Relic, Inc.) uses.

It is **not** known what communication or at rest encryption the transaction
mailing service Mailgun (Sinch America, Inc.) uses.

# Application implementation controls

## List of data

Please review the [privacy policy](/privacy) for a detailed listing of sensitive
data handled by the Product.

## Data flow diagram

All user submitted data goes from the Product's frontend served from
www.projectifyapp.com to the API served from api.projectifyapp.com to the
various backend services:

```
                .----------.
      .---------|Cloudinary|
      |         .---+------.
      |             |         .----------.
      |             .---------+PostgreSQL|
      |             |         .----------.
  .---+----.    .---+---.     .-----.
  |Frontend+----+Backend+-----+Redis|
  .--------.    .---+---.     .-----.
                    |         .---------.
                    +---------+New Relic|
                    |         .---------.
                    |         .----------.
                    +---------+Papertrail|
                    |         .----------.
                    |         .--------.
                    .---------+Sendgrid|
                              .--------.
```

## Vulnerability prevention

The Product uses access controls to prevent users from accessing data or
admin features that they are not authorized to.

Session IDs are handled using secure and HTTP-only cookies.

SQL Injections are prevented using the Django ORM.

Cross site scripting is prevented by using Svelte frontend templating and only
allowing raw HTML where it is used as part of translation and there ensuring no
user submittable content is used for translation.

**No** measures have been taken to mitigate cross-site request forgery (CSRF).

The usage of vulnerable libraries is monitored using Dependabot.

## Time to fix vulnerabilities

Any known vulnerabilities will be patched within 90 days of discovery.

## Build process

The build and deploy process is fully automated. Any dependencies used in the
Product are included in a reproducible way using NPM and Poetry lock files.

# Operational controls

## Physical access

All of the Product's infrastructure is hosted by third parties which in turn
implement strict physical access controls.

## Logical access

Only Product administrators with a legitimate need have access to the Product's
infrastructure or admin site.

Administrative accounts that are no longer needed are deactivated in a timely
manner.

We regularly review administrative accounts and only grant administrative
privileges to administrators where absolutely necessary.

Administrative access to the Product's infrastructure is only possible using
Multi-Factor Authentication (MFA).

Administrative access to the Product's admin site at
api.projectifyapp.com/admin is **not** secured by MFA.

## Subprocessors

A list of all subprocessors is available in the [GDPR section of the privacy
policy](/privacy) under **Article 6 (Cross-Border Data Transfer)**.

## Backup and Disaster Recovery

Heroku Postgres has continuous rollbacks enabled spanning 4 days. Daily backups
at 00:00 UTC for the production PostgreSQL database are enabled.

Assets stored with Cloudinary are **not** backed up.

**No** steps have been taken to maintain and test disaster recovery plans.

**No** steps have been taken to periodically test backup restoration.

# Inquiries

Should You have any questions, please [contact Us](/contact-us).
