<p>
    <img alt="Rolls-Royce Logo" width="100" src="https://raw.githubusercontent.com/rropen/MEC/main/src/frontend/public/logo4.png">
    <br>
    Project to separate the <i>Team Creation</i> functionality from <a href="https://github.com/rropen/absense-planner" >absence-planner</a>.
</p>
<p>
<a href="https://ubiquitous-chainsaw-e069ab7b.pages.github.io/"><img src="https://img.shields.io/badge/Rolls--Royce-Software%20Factory-10069f"></a>
</p>
<p>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen?style=flat"></a>
</p>

# Team App

---

## Usage

### Overview

Project to separate the _Team Creation_ functionality from [absence-planner](https://github.com/rropen/absense-planner).

It is a headless server that provides a [Django REST API](https://www.django-rest-framework.org/) to interact with teams and team members.

### Running the Server

Once you have followed the [instructions in the Developer Guide for setting up the application](DEVELOPER.md#setup), you can simply run the server with `uv`:

```shell
uv run teams_source/manage.py runserver
```

If you are jumping from setup to this and the system cannot find the `uv` command, you may have to restart your IDE or device.

## Contacts

Contact [Oli Rowan](mailto:Oli.Rowan@Rolls-Royce.com) if you have any questions or want help adapting this for another situation.

## Developer Guide

To get started with the Absence Planner and the Team App, we have a [developer guide](DEVELOPER.md).

## Contributing

To learn more about contributing (e.g., commits, pull requests, etc.), read our [Contributer's Guide](CONTRIBUTING.md)

## Colour Schemes

- Options for modifying colour schemes can be found in the profile settings page, under the "App Information" category. Different colours can be picked for altering Bank Holidays and Weekends. A dropdown list within the same container can be modified to choose whether these specific dates are shown on the calendar. The rectangular bar can be selected to show a colour picker where a specific colour can be chosen, after these changes have been made they can be confirmed by clicking on the "Submit" button to apply them.
