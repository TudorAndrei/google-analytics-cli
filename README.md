# Google Analytics CLI (Experimental)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![YouTube Video Views](https://img.shields.io/youtube/views/PT4wGPxWiRQ)](https://www.youtube.com/watch?v=PT4wGPxWiRQ)

This repo contains a local CLI that interacts with the
[Google Analytics](https://support.google.com/analytics) Admin and Data APIs.

GitHub: https://github.com/TudorAndrei/google-analytics-cli

Join the discussion and ask questions on
[Discord](https://discord.com/channels/971845904002871346/1398002598665257060).

## Commands 🛠️

The CLI uses the
[Google Analytics Admin API](https://developers.google.com/analytics/devguides/config/admin/v1)
and
[Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
to provide a set of commands.

### Retrieve account and property information 🟠

- `account-summaries`: Retrieves information about the user's Google
  Analytics accounts and properties.
- `property-details`: Returns details about a property.
- `google-ads-links`: Returns a list of links to Google Ads accounts for
  a property.
- `property-annotations`: Returns annotations for a property.

### Run core reports 📙

- `report`: Runs a Google Analytics report using the Data API.
- `custom-dimensions-metrics`: Retrieves the custom dimensions and
  metrics for a specific property.

### Run realtime reports ⏳

- `realtime-report`: Runs a Google Analytics realtime report using the
  Data API.

## Setup instructions 🔧

✨ Watch the [Google Analytics CLI Setup
Tutorial](https://youtu.be/nS8HLdwmVlY) on YouTube for a step-by-step
walkthrough of these instructions.

[![Watch the video](https://img.youtube.com/vi/nS8HLdwmVlY/mqdefault.jpg)](https://www.youtube.com/watch?v=nS8HLdwmVlY)

Setup involves the following steps:

1.  Configure Python.
1.  Configure credentials for Google Analytics.
1.  Add credentials to a `.env` file.

### Configure Python 🐍

[Install pipx](https://pipx.pypa.io/stable/#install-pipx).

### Enable APIs in your project ✅

[Follow the instructions](https://support.google.com/googleapi/answer/6158841)
to enable the following APIs in your Google Cloud project:

* [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com)
* [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)

### Configure credentials 🔑

Configure your [Application Default Credentials
(ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc).
Make sure the credentials are for a user with access to your Google Analytics
accounts or properties.

Credentials must include the Google Analytics read-only scope:

```
https://www.googleapis.com/auth/analytics.readonly
```

Check out
[Manage OAuth Clients](https://support.google.com/cloud/answer/15549257)
for how to create an OAuth client.

Here are some sample `gcloud` commands you might find useful:

- Set up ADC using user credentials and an OAuth desktop or web client after
  downloading the client JSON to `YOUR_CLIENT_JSON_FILE`.

  ```shell
  gcloud auth application-default login \
    --scopes https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform \
    --client-id-file=YOUR_CLIENT_JSON_FILE
  ```

- Set up ADC using service account impersonation.

  ```shell
  gcloud auth application-default login \
    --impersonate-service-account=SERVICE_ACCOUNT_EMAIL \
    --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform
  ```

When the `gcloud auth application-default` command completes, copy the
`PATH_TO_CREDENTIALS_JSON` file location printed to the console in the
following message. You'll need this for the next step!

```
Credentials saved to file: [PATH_TO_CREDENTIALS_JSON]
```

### Configure `.env`

Copy `.env.example` to `.env` in the project root (or in your current working
directory), and set the path to your credentials JSON:

```dotenv
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/credentials.json
GOOGLE_PROJECT_ID=your-project-id
```

### Optional: load `.env` automatically with direnv

If you use [direnv](https://direnv.net/), this repo includes `.envrc` with:

```shell
dotenv
```

Enable it once in the project directory:

```shell
direnv allow
```

## Try it out 🥼

Install and run:

```shell
pip install -e .
analytics-cli --help
```

Examples:

- List account summaries:

  ```shell
  analytics-cli account-summaries
  ```

- Get property details:

  ```shell
  analytics-cli property-details 123456789
  ```

- Run a core report:

  ```shell
  analytics-cli report 123456789 \
    --date-ranges '[{"start_date":"7daysAgo","end_date":"yesterday"}]' \
    --dimension eventName \
    --metric eventCount
  ```

- Run a realtime report:

  ```shell
  analytics-cli realtime-report 123456789 \
    --dimension country \
    --metric activeUsers
  ```

## Contributing ✨

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).
