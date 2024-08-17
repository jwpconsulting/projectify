# Changelog

## 2024.8.17

### Changed

- Change frontend `.env.template` file to assume all backend requests are
  proxied through vite server.

### Fixed

- Fix label creation failing because of missing $currentWorkspace
- Fix missing general validation message when creating and updating labels
