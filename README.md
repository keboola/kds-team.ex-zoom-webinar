Zoom Webinars
=============

Description

**Table of contents:**

[TOC]

Functionality notes
===================

Prerequisites
=============

Authorize access to your Zoom account under the Authorization tab.


Supported endpoints
===================

Currently, the component supports the following endpoints:
- Webinar registrants - [documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrants)
- Registration questions - [documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantsQuestionsGet)
- Polls - [documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarPolls)
- Survey - [documentation](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyGet)

If you need more endpoints, please submit your request to

Configuration
=============

Select a webinar and endpoints from which you want to retrieve data.

Output
======

The component creates one output table for each selected endpoint.

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to
your custom path in the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following
command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone https://bitbucket.org/kds_consulting_team/kds-team.ex-zoom-webinars kds-team.ex-zoom-webinars
cd kds-team.ex-zoom-webinars
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers
documentation](https://developers.keboola.com/extend/component/deployment/)
