# Changelog

## 2024.8.20

### Fixed

- Internal ordering of tasks was inverted. This prevented users from properly
moving tasks to the top/bottom.

## 2024.8.17

### Changed

- Change frontend `.env.template` file to assume all backend requests are
  proxied through vite server.

### Fixed

- Fix label creation failing because of missing $currentWorkspace
- Fix missing general validation message when creating and updating labels
- Fix outdated Twisted version to 24.7.0
- Fix outdated Django version to 5.1
