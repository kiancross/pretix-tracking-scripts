# pretix-tracking-scripts

[![PyPI version](https://badge.fury.io/py/pretix-tracking-scripts.svg)](https://pypi.org/project/pretix-tracking-scripts/)
[![License](https://img.shields.io/github/license/kiancross/pretix-tracking-scripts)](https://github.com/kiancross/pixy/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/kiancross/pretix-tracking-scripts/graph/badge.svg?token=PHpYdVTJ3H)](https://codecov.io/gh/kiancross/pretix-tracking-scripts)

This plugin for [pretix](https://github.com/pretix/pretix) enables the addition of tracking scripts, including [Google Analytics](https://developers.google.com/analytics) and [Meta Pixel](https://www.facebook.com/business/tools/meta-pixel), to your store. It supports cookie consent but does not hide sensitive URLs, unlike the [official pretix solution](https://behind.pretix.eu/2019/02/02/trackers/).

## Installation

 1. Install the plugin:

    ```bash
    pip install pretix-tracking-scripts
    ```

 2. Enable the plugin on your event page.

 3. Once enabled, a new Settings link will appear in the event settings side-navigation bar. Use this to configure your tracking scripts:

     * Enter a Google Analytics Measurement ID.
     * Enter a Meta Pixel dataset ID.
    
    Tracking scripts are only included when a value is provided.

> [!IMPORTANT]
> This plugin does not specify any pretix version constraints. It is intended to remain compatible with future pretix releases, and adding explicit version limits would unnecessarily restrict where it can be used. The plugin has been explicitly tested with pretix `2025.10.1`. If you encounter any issues when using it with a later pretix release, please [open an issue](https://github.com/kiancross/pretix-tracking-scripts/issues/new) on this repository.

## Development

 1. Ensure you have a working [pretix development setup](https://docs.pretix.eu/en/latest/development/setup.html).

 2. Clone this repository.

 3. Install the plugin and dependencies:

    ```bash
    poetry install
    ```

If Pretix is not running within a virtual Python environment, or if your plugin and Pretix are operating in separate environments, you may want to install this plugin globally using the following command:

```bash
pip install -e .
```

### Code Styling

To automate code styling, run the following commands:

```bash
poetry run isort .
poetry run black .
```

### Automated Testing

To execute the automated tests, run the following command:

```bash
poetry run py.test tests
```
